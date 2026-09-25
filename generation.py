def generation(prompt, llm):
    response = llm.invoke(prompt)
    return response