"""
Configuration settings for TravelBuddy Travel Agent
"""

import os
from dotenv import load_dotenv

load_dotenv()

# ============================================
# LLM Configuration
# ============================================
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4o-mini")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise ValueError("❌ OPENAI_API_KEY not found in .env file. Please add it.")

# ============================================
# Paths
# ============================================
SYSTEM_PROMPT_PATH = "system_prompt.txt"

# ============================================
# Agent Settings
# ============================================
AGENT_NAME = "TravelBuddy"
AGENT_DESCRIPTION = "Trợ lý du lịch thông minh cho Việt Nam"
MAX_ITERATIONS = 10  # Maximum tool calls in one conversation turn

# ============================================
# Cities Available
# ============================================
AVAILABLE_CITIES = [
    "Hà Nội",
    "Hồ Chí Minh",
    "Đà Nẵng",
    "Phú Quốc"
]

# ============================================
# Debug Settings
# ============================================
DEBUG = os.getenv("DEBUG", "False").lower() == "true"
VERBOSE = os.getenv("VERBOSE", "True").lower() == "true"
