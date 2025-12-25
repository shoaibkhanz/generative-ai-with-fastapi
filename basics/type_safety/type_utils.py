from typing import Annotated, Literal

import tiktoken
from loguru import logger

# Using TypeAlias and Literal
# SupportedModels: TypeAlias = Literal["anthropic.claude-3-5-sonnet-20241022-v2:0"]

# Using new `type` and Literal
# type SupportedModels = Literal["anthropic.claude-3-5-sonnet-20241022-v2:0"]
# type PriceTable = dict[SupportedModels, float]

type SupportedModels = Annotated[
    Literal["anthropic.claude-3-5-sonnet-20241022-v2:0"], "Supported Text Models"
]
type PriceTable = Annotated[
    dict[SupportedModels, float], "Supported Model Pricing Table"
]

price_table: PriceTable = {"anthropic.claude-3-5-sonnet-20241022-v2:0": 0.05}


def count_tokens(text: str | None) -> int:
    if text is None:
        logger.warning("Response is None, Assuming 0 tokens used.")
        return 0
    enc = tiktoken.encoding_for_model("gpt-4o")
    return len(enc.encode(text))


def calculate_usage_costs(
    prompt: str, response: str | None, model: SupportedModels
) -> tuple[float, float, float]:
    if model not in price_table:
        raise ValueError(f"cost calculation is not supported for the {model} model")
    price = price_table[model]
    req_costs = price * count_tokens(prompt) / 1000
    res_costs = price * count_tokens(response) / 1000
    total_costs = req_costs + res_costs
    return req_costs, res_costs, total_costs
