import os
import logging
from openai import AsyncOpenAI
from ragas.llms import llm_factory
from ragas.embeddings.base import embedding_factory
from typing import Dict, List

logger = logging.getLogger(__name__)

# RAGAS imports
try:
    from ragas.metrics.collections import AnswerRelevancy, Faithfulness
    from ragas import evaluate
    RAGAS_AVAILABLE = True
except ImportError:
    RAGAS_AVAILABLE = False
    logger.warning(f"RAGAS is not available.")


VOCARUM_BASE_URL = "https://openai.vocareum.com/v1"
LLM_MODEL = "gpt-4o-mini"
EMBEDDING_MODEL = "text-embedding-3-small"


async def evaluate_response_quality(question: str, answer: str, contexts: List[str]) -> Dict[str, float]:
    """Evaluate response quality using RAGAS metrics"""
    if not RAGAS_AVAILABLE:
        return {"error": "RAGAS not available"}


    #Check RAGAS availability
    if not RAGAS_AVAILABLE:
        return {
            "error": "RAGAS not available"
        }

    #Validate input
    if not question or not question.strip():
        return {
            "error": "Question is empty"
        }

    if not answer or not answer.strip():
        return {
            "error": "Answer is empty"
        }

    if not contexts:
        return {
            "error": "No contexts were provided"
        }

    # Remove empty contexts
    contexts = [
        context
        for context in contexts
        if context and context.strip()
    ]

    if not contexts:
        return {
            "error": "All contexts are empty"
        }

    
    # TODO: Create evaluator LLM with model gpt-3.5-turbo
    openai_api_key = os.getenv("OPENAI_API_KEY")

    if not openai_api_key:
        return {
            "error": "OPENAI_API_KEY or CHROMA_OPENAI_API_KEY is not set"
        }


    # TODO: Create evaluator_embeddings with model test-embedding-3-small

    try:
        client = AsyncOpenAI(
            api_key=openai_api_key,
            base_url=VOCARUM_BASE_URL
        )

        evaluator_llm = llm_factory(
            model=LLM_MODEL,
            client=client
        )
     
        evaluator_embeddings = embedding_factory(
            "openai",
             model=EMBEDDING_MODEL,
             client=client
        )


    # TODO: Define an instance for each metric to evaluate

        faithfulness_metric = Faithfulness(
            llm=evaluator_llm
        )

        response_relevancy_metric = AnswerRelevancy(
            llm=evaluator_llm,
            embeddings=evaluator_embeddings
        )


    # TODO: Evaluate the response using the metrics

        results: Dict[str, float] = {}

        # Faithfulness
        
        try:
            faithfulness_score = await faithfulness_metric.ascore(
                    user_input=question,
                    response=answer,
                    retrieved_contexts=contexts
                    )
            

            results["faithfulness"] = float(faithfulness_score)


        except Exception as e:
            logger.exception(
                "Faithfulness evaluation failed"
            )
            results["faithfulness"] = 0.0

        #Response Relevancy
        
        try:
            relevancy_score = await response_relevancy_metric.ascore(
                user_input=question,
                response=answer
                )
            

            results["response_relevancy"] = float(relevancy_score)

        except Exception as e:
            logger.exception(
                "Response relevancy evaluation failed"
            )
            results["response_relevancy"] = 0.0


    # TODO: Return the evaluation results
        return results

    except Exception as e:

        logger.exception(
            "Error during RAG evaluation"
        )

        return {
            "error": str(e)
        }    
