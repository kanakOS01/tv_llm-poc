import tiktoken

def count_prompt_tokens(prompt: str, model: str) -> int:
    encoding = tiktoken.encoding_for_model(model)
    return len(encoding.encode(prompt))

def count_prompt_tokens_from_file(prompt_file: str, model: str) -> int:
    with open(prompt_file, "r") as f:
        prompt = f.read()
    return count_prompt_tokens(prompt, model)


# testing, not to be run as a script
if __name__ == "__main__":
    print(count_prompt_tokens_from_file("/home/kanak/Desktop/GSOC/Python/tolvera/tv_llm-poc/apilist.txt", "gpt-4o-mini"))