# coding: utf-8
# Copyright (c) 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.

##########################################################################
# generate_text_demo1.py
# Supports Python 3
##########################################################################
# Info:
# Get texts from LLM model for given prompts using OCI Generative AI Service.
##########################################################################
# Application Command line(no parameter needed)
# python generate_text_demo.py
##########################################################################
import oci

from config import (COMPARTMENT_OCID)

# these parameters control text generation from LLM and creativity
from llm_gen_config import (MAX_TOKENS,
                           TOP_K,
                           TEMPERATURE,
                           FREQUENCY_PENALTY)


#
# Configs
#

# Setup basic variables
# Auth Config
# TODO: Please update config profile name and use the compartmentId that has policies grant permissions for using Generative AI Service
compartment_id = COMPARTMENT_OCID

# the model
MODEL_ID = "cohere.command"

# to access API keys for auth
CONFIG_PROFILE = "DEFAULT"
config = oci.config.from_file('~/.oci/config', CONFIG_PROFILE)

# Service endpoint
ENDPOINT = "https://generativeai.aiservice.us-chicago-1.oci.oraclecloud.com"

generative_ai_client = oci.generative_ai.GenerativeAiClient(config=config, service_endpoint=ENDPOINT, 
                                                            retry_strategy=oci.retry.NoneRetryStrategy(), 
                                                            timeout=(10,240))


#
# Functions
#
def read_prompt(file_name):
    print("")
    print(f"Reading prompt from {file_name}.")

    with open(file_name, "r") as file:
        # Get the lines from the file
        lines = file.readlines()

    # Put the lines into a single variable
    text = "".join(lines)

    print(text)

    return text

# this is the input prompt. It is written in prompts.txt
PROMPT = read_prompt("prompts.txt")
prompts = [PROMPT]

# to use these functionalitis we need to use the OCI for the OCI GenAI Limited Availability
generate_text_detail = oci.generative_ai.models.GenerateTextDetails()
generate_text_detail.prompts = prompts
generate_text_detail.serving_mode = oci.generative_ai.models.OnDemandServingMode(model_id=MODEL_ID)
# generate_text_detail.serving_mode = oci.generative_ai.models.DedicatedServingMode(endpoint_id="custom-model-endpoint") # for custom model from Dedicated AI Cluster
generate_text_detail.compartment_id = compartment_id

# setting LLM params for text generation
generate_text_detail.max_tokens = MAX_TOKENS
generate_text_detail.top_k = TOP_K
generate_text_detail.temperature = TEMPERATURE
generate_text_detail.frequency_penalty = FREQUENCY_PENALTY


if "<compartment_ocid>" in compartment_id:
    print("ERROR:Please update your compartment id in target python file")
    quit()

generate_text_response = generative_ai_client.generate_text(generate_text_detail)

output_lists = generate_text_response.data.generated_texts

# Print result
print("**************************Generate Texts Result**************************")
print()

for gen_text_array in output_lists:
    for elem in gen_text_array:
        print(elem.text)

print()
