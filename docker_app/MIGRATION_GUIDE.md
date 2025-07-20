# Migration Guide: Simplified Assistant Architecture

This guide explains the changes made to the assistant architecture and how to migrate from the previous implementation.

## Architecture Changes

### 1. Consolidated Assistants

We've consolidated the 15+ individual assistants into 5 core domain assistants:

| Core Domain | Previous Assistants |
|-------------|---------------------|
| Business & Finance | financial_assistant, business_assistant, economics_assistant, cryptocurrency_assistant, entrepreneurship_assistant, tokenomics_assistant, international_finance_assistant, company_intelligence_assistant |
| Technology & Security | tech_assistant, security_assistant, computer_science_assistant, ai_assistant, blockchain_assistant, web3_assistant, cybersecurity_defense_assistant, cybersecurity_offense_assistant, cryptography_assistant, aws_assistant |
| Research & Knowledge | research_assistant, web_browser_assistant, data_analysis_assistant, predictive_analysis_assistant, english_assistant, math_assistant |
| Specialized Industries | aviation_assistant, formula1_assistant, sports_assistant, louisiana_legal_assistant, automotive_assistant |
| Universal | universal_assistant, general_assistant, no_expertise |

### 2. Simplified Routing

The routing logic has been simplified from multiple files to a single `unified_router.py` file that:
- Uses domain detection to route queries to the appropriate core assistant
- Maintains specialized routing for high-priority domains
- Provides backward compatibility with legacy assistants

### 3. UI Changes

The UI now defaults to "Core Domains (Auto-Route)" mode, which uses only the 5 core domain assistants. The "Advanced Configuration" mode still allows access to all legacy assistants.

## Migration Steps for Users

1. **Default Usage**: No action required. Queries will automatically be routed to the appropriate core domain assistant.

2. **Advanced Configuration**: If you previously used specific assistants, you can still access them in "Advanced Configuration" mode.

3. **Custom Integrations**: If you had custom integrations with specific assistants, update them to use the corresponding core domain assistant:
   - Financial integrations → Business & Finance Assistant
   - Technology integrations → Technology & Security Assistant
   - Research integrations → Research & Knowledge Assistant
   - Industry-specific integrations → Specialized Industries Assistant
   - General integrations → Universal Assistant

## Migration Steps for Developers

1. **Assistant References**: Update references from specific assistants to core domain assistants:
   ```python
   # Old
   from financial_assistant import financial_assistant
   
   # New
   from unified_assistants import business_finance_assistant
   ```

2. **Routing Logic**: Update routing logic to use the unified router:
   ```python
   # Old
   from smart_router import smart_route
   assistant_func, enhanced_prompt = smart_route(prompt, datetime_context, assistants)
   
   # New
   from unified_router import unified_route
   assistant_func, enhanced_prompt = unified_route(prompt, datetime_context, assistants)
   ```

3. **Assistant Mapping**: Update assistant mappings to include core domain assistants:
   ```python
   # Old
   assistants = {
       'financial': financial_assistant,
       'tech': tech_assistant,
       # ...
   }
   
   # New
   assistants = {
       'business_finance': business_finance_assistant,
       'tech_security': tech_security_assistant,
       # ...
   }
   ```

## Backward Compatibility

All legacy assistants are still available and can be enabled in Advanced Configuration mode. This ensures backward compatibility with existing code and user preferences.