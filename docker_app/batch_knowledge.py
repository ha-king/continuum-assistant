"""
Batch Knowledge - Efficient batch processing for knowledge storage
"""

import os
from strands import Agent
from strands_tools import memory, use_llm
from collections import deque
import threading
import time

class BatchKnowledgeProcessor:
    """Process knowledge items in batches for efficiency"""
    
    def __init__(self, batch_size=5, max_queue_size=100, flush_interval=60):
        self.queue = deque(maxlen=max_queue_size)
        self.batch_size = batch_size
        self.flush_interval = flush_interval  # seconds
        self.lock = threading.Lock()
        self.last_flush_time = time.time()
        
        # Start background thread for periodic flushing
        self.flush_thread = threading.Thread(target=self._periodic_flush, daemon=True)
        self.flush_thread.start()
    
    def add_item(self, content, context):
        """Add an item to the queue for batch processing"""
        if not os.environ.get("KNOWLEDGE_BASE_ID"):
            return
        
        with self.lock:
            self.queue.append((content, context))
            
            # Process immediately if batch size reached
            if len(self.queue) >= self.batch_size:
                self._process_batch()
    
    def _process_batch(self):
        """Process a batch of knowledge items"""
        if not self.queue:
            return
        
        try:
            # Create agent once for the batch
            agent = Agent(tools=[memory, use_llm])
            
            # Process items in current queue
            items = []
            with self.lock:
                while self.queue and len(items) < self.batch_size:
                    items.append(self.queue.popleft())
            
            # Check for existing similar content before storing
            for content, context in items:
                try:
                    # Check if similar content exists
                    existing = agent.tool.memory(
                        action="retrieve", 
                        query=content[:100], 
                        min_score=0.8, 
                        max_results=1
                    )
                    
                    # Only store if not redundant
                    if not existing or len(str(existing).strip()) < 50:
                        agent.tool.memory(
                            action="store", 
                            content=f"{context}\nLearned: {content}"
                        )
                except Exception as e:
                    print(f"Error storing knowledge item: {str(e)}")
                    
            print(f"Processed batch of {len(items)} knowledge items")
            
        except Exception as e:
            print(f"Error in batch knowledge processing: {str(e)}")
    
    def _periodic_flush(self):
        """Periodically flush the queue even if not full"""
        while True:
            time.sleep(5)  # Check every 5 seconds
            
            current_time = time.time()
            if current_time - self.last_flush_time > self.flush_interval and self.queue:
                self._process_batch()
                self.last_flush_time = current_time
    
    def flush(self):
        """Manually flush the queue"""
        with self.lock:
            self._process_batch()
            self.last_flush_time = time.time()

# Global instance
knowledge_processor = BatchKnowledgeProcessor()

def store_knowledge_batch(content, query_context):
    """Store knowledge using batch processor"""
    knowledge_processor.add_item(content, query_context)

def flush_knowledge_queue():
    """Manually flush the knowledge queue"""
    knowledge_processor.flush()