def python_function_basic(*, name: str, env: str):
    return f"""name: {name} 
env: {env}
python:
  call: <required, module:function to call>
  requirements: <optional, path to requirements.txt>
"""
