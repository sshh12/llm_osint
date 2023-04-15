SUMMARY_TASK_PROMPT = "Then list all the information you have gathered and where these details were gathered from. Be VERY detailed and list as much information as possible."

INITIAL_WEB_AGENT_PROMPT = f"""
{{gather_prompt}}
            
{SUMMARY_TASK_PROMPT}
"""

DEEP_DIVE_LIST_PROMPT = """
Given these details about {name} and search and webpage reading abilities, create a list of {num_topics} areas to deep dive into to better "{gather_prompt}".

Format the areas as a numbered list. Respond only with the list.

Details:
{current_knowlege}
"""

DEEP_DIVE_WEB_AGENT_PROMPT = f"""
{{gather_prompt}}

Here's what you already know:
{{current_knowlege}}

{SUMMARY_TASK_PROMPT}

For now, specifically ONLY look into: {{deep_dive_topic}}
"""
