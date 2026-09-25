import torch
def generate_text(image, processor, model):
    image = image.convert('RGB')
    message = [
        {
            'role': 'user',
            'content': [
                {
                    'type': 'image',
                    'image': image
                },
                {
                    'type': 'text',
                    'text': (
                        'Describe the image in detail. '
                        'If the image contains numerical values, tables, labels, '
                        'or ordered information, capture them accurately. '
                        'If the image contains other visual elements, describe them '
                        'clearly so a human can understand the image from the text alone. '
                        'Focus on extracting important information that would be useful '
                        'for retrieval and question answering.'
                    )
                }
            ]
        }
    ]
    text = processor.apply_chat_template(
        message, tokenize = False, add_generation_prompt = True
    )
    input = processor(text = [text], image = [image], return_tensors = 'pt')
    input = {k: v.to(model.device) for k, v in input.items()}
    with torch.no_grad():
        generated_tokens = model.generate(**input, max_new_tokens = 512, repetition_penalty = 1.1)
    input_len = input['input_ids'].shape[1]
    new_tokens = generated_tokens[0][input_len:]
    output = processor.decode(new_tokens, skip_special_tokens = True)
    return output.strip()