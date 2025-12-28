# Text chunking logic for ingestion pipeline

import re
from typing import List


class TextChunker:
    """
    Handles chunking of text content into smaller pieces for embedding
    """
    
    def __init__(self, max_chunk_size: int = 1000, overlap: int = 200):
        self.max_chunk_size = max_chunk_size
        self.overlap = overlap

    def chunk_text(self, text: str) -> List[str]:
        """
        Splits text into overlapping chunks of specified size
        """
        chunks = []
        
        # Simple sentence-based chunking
        sentences = re.split(r'[.!?]+', text)
        
        current_chunk = ""
        for sentence in sentences:
            sentence = sentence.strip()
            if not sentence:
                continue
                
            if len(current_chunk + " " + sentence) <= self.max_chunk_size:
                current_chunk += " " + sentence
            else:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                
                # Start a new chunk, possibly with overlap
                if len(sentence) > self.max_chunk_size:
                    # If a single sentence is too long, split by length
                    for i in range(0, len(sentence), self.max_chunk_size - self.overlap):
                        chunk = sentence[i:i + self.max_chunk_size - self.overlap]
                        chunks.append(chunk)
                    current_chunk = ""
                else:
                    # Start new chunk with overlap from previous
                    if chunks and len(chunks[-1]) > self.overlap:
                        overlap_text = chunks[-1][-self.overlap:]
                        current_chunk = overlap_text + " " + sentence
                    else:
                        current_chunk = sentence
        
        if current_chunk:
            chunks.append(current_chunk.strip())
            
        return chunks