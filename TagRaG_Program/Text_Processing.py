
# import pandas as pd
# from langchain_community.llms import Ollama
# from LanguageText_Model import processLanguageModel_Text

# def process_dataframe(doc_path, model_type, user_prompt, word_count, data_types):
#     cached_llm = Ollama(model=model_type)
#     df_data = pd.read_csv(doc_path)
    
#     dataRes = []
#     prompt = df_data.shape[0] * user_prompt

#     for index, text in enumerate(df_data["Text"].values):
#         result = processLanguageModel_Text(text, model_type, user_prompt, index)
#         dataRes.append(result)

#     df_data["prompt_results"] = dataRes
#     df_data["prompt"] = user_prompt

#     if len(data_types) == 0:
#         return df_data
#     else:
#         tags = []
#         for text in df_data["prompt_results"].values:
#             if word_count == 1:
#                 classification_prompt = f"""Classify the following text based on the given tags:
                
# Text: {text}
                
# Available Tags: {', '.join(data_types)}
                
# Please assign the most suitable tag to this text. Respond with only the tag."""

#                 response = cached_llm.invoke(classification_prompt)
#                 tag = response.strip().split()[0]
#                 tags.append(tag)

#             elif word_count == 2:
#                 classification_prompt = f"""Classify the following text based on the given tags:
                
# Text: {text}
                
# Available Tags: {', '.join(data_types)}
                
# Please assign the most suitable two tags to this text. Respond with only the tags, separated by a comma."""

#                 response = cached_llm.invoke(classification_prompt)
#                 tag_list = response.strip().split(',')
#                 tag_list = [tag.strip() for tag in tag_list[:2]]
#                 tags.append(', '.join(tag_list))

#         df_data["tags"] = tags
#         return df_data



import os
import pandas as pd
from langchain_community.llms import Ollama
from LanguageText_Model import processLanguageModel_Text

def process_dataframe(doc_path, model_type, user_prompt, word_count, data_types):
    # Initialize the model
    cached_llm = Ollama(model=model_type)
    
    # Load the CSV file
    df_data = pd.read_csv(doc_path)
    
    # Process each text and classify
    dataRes = []
    
    # Process each text and store results
    for index, text in enumerate(df_data["Text"].values):
        result = processLanguageModel_Text(text, model_type, user_prompt, index)
        dataRes.append(result)
    
    # Add results and prompt to DataFrame
    df_data["Prompt_Results"] = dataRes
    df_data["prompt"] = user_prompt
    
    # If no data_types are provided, return the DataFrame without tags
    if len(data_types) == 0:
        return df_data
    
    # Initialize tags list
    tags = []
    
    for text in df_data["Prompt_Results"].values:
        if word_count == 0:
            tags.append("")  # Append an empty string for 0 tags
            continue
        
        elif word_count == 1:
            classification_prompt = f"""Classify the following text based on the given tags:
                
            Text: {text}
            
            Available Tags: {', '.join(data_types)}
            
            Please assign the most suitable tag to this text. Respond with only the tag."""
    
            response = cached_llm.invoke(classification_prompt)
            tag = response.strip().split()[0]  # Extract the first word from the response
            tags.append(tag)
    
        elif word_count == 2:
            classification_prompt = f"""Classify the following text based on the given tags:
                
            Text: {text}
            
            Available Tags: {', '.join(data_types)}
            
            Please assign the most suitable two tags to this text. Respond with only the tags, separated by a comma."""
    
            response = cached_llm.invoke(classification_prompt)
            tag_list = response.strip().split(',')
            tag_list = [tag.strip() for tag in tag_list[:2]]  # Ensure we only take the required number of tags
            tags.append(', '.join(tag_list))
        
        elif word_count == 3:
            classification_prompt = f"""Classify the following text based on the given tags:
                
            Text: {text}
            
            Available Tags: {', '.join(data_types)}
            
            Please assign the most suitable three tags to this text. Respond with only the tags, separated by a comma."""
    
            response = cached_llm.invoke(classification_prompt)
            tag_list = response.strip().split(',')
            tag_list = [tag.strip() for tag in tag_list[:3]]  # Ensure we only take the required number of tags
            tags.append(', '.join(tag_list))
    
    # Only add the tags column if tags list is not empty
    if tags:
        df_data["tags"] = tags
    
    # Return the DataFrame (with or without tags)
    return df_data