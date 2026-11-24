from app.observability import trace
import logging
import time 
from functools  import lru_cache
from pinecone import Pinecone, ServerlessSpec
from app.config import settings
 
log = logging.getLogger(__name__)