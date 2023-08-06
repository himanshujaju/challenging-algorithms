from enum import Enum
from typing import Optional
from dataclasses import dataclass

class _BufferType(Enum):
    ORIGINAL = 1
    ADDED = 2

@dataclass
class _Piece:
    type: _BufferType
    offset: int
    length: int

class PieceTable:
    def __init__(self, original_doc: str):
        self._original = original_doc
        self._addBuffer = ""
        self._pieces = [_Piece(_BufferType.ORIGINAL, 0, len(original_doc))]
        self._totalLength = len(original_doc)

    def insert(self, position: int, text: str) -> None:
        # Prepare the piece
        original_length = self._totalLength
        piece_to_add = _Piece(_BufferType.ADDED, len(self._addBuffer), len(text))
        self._addBuffer += text
        self._totalLength += piece_to_add.length

        if text == "Wonderful ":
            print(original_length, len(self._pieces))

        if position == original_length:
            # Append to the end
            self._pieces.append(piece_to_add)
            return

        current_length = 0
        for index, piece in enumerate(self._pieces):
            if position == current_length:
                # Simple insert
                self._pieces.insert(index, piece_to_add)
                return

            if position > current_length and position < current_length + piece.length:
                # Split current piece into two, and then insert curr_1, to_add, curr_2
                left_piece = _Piece(piece.type, piece.offset, position - current_length)
                right_piece = _Piece(piece.type, piece.offset + left_piece.length, piece.length - left_piece.length)

                self._pieces = self._pieces[0:index] + [left_piece, piece_to_add, right_piece] + self._pieces[index + 1:]
                return
            
            current_length += piece.length
            
        # If this line is reached, then there is a bug!
        assert(False)

    def delete(self, start: int, end: int) -> None:
        new_length = 0
        new_pieces = []

        current_length = 0
        for piece in self._pieces:
            piece_start = current_length
            piece_end = current_length + piece.length

            current_length += piece.length

            if piece_start >= end or piece_end <= start:
                new_length += piece.length
                new_pieces.append(piece)
            
            if piece_start >= start and piece_end <= end:
                # Delete entire piece
                continue

            # We need to break up the piece and keep one part.
            if start >= piece_start and start < piece_end:
                left_start = piece_start
                left_end = start
                left_piece = _Piece(piece.type, left_start - piece_start, left_end - left_start)
                if left_piece.length > 0:
                    new_pieces.append(left_piece)
                    new_length += left_piece.length

            if end > piece_start and end <= piece_end:
                right_start = end
                right_end = piece_end
                right_piece = _Piece(piece.type, right_start - piece_start, right_end - right_start)
                if right_piece.length > 0:
                    new_pieces.append(right_piece)
                    new_length += right_piece.length

        self._totalLength = new_length
        self._pieces = new_pieces

    def getText(self) -> str:
        ret = ""
        for piece in self._pieces:
            ret += self._getPieceText(piece)
        return ret

    def retrieve(self, start: int, end: int) -> Optional[str]:
        if start < 0 or end > self._totalLength:
            return None

        ret = ""
        current_length = 0
        for piece in self._pieces:
            piece_start = current_length
            piece_end = current_length + piece.length

            if piece_start > end:
                break
            if piece_end < start:
                continue

            piece_text = self._getPieceText(piece)

            common_start = max(start, piece_start) - piece_start
            common_end = min(end, piece_end) - piece_start

            ret += piece_text[common_start:common_end]
        return ret

    def _getPieceText(self, piece: _Piece) -> str:
        start = piece.offset
        end = piece.offset + piece.length

        if piece.type == _BufferType.ORIGINAL:
            return self._original[start:end]
        else:
            return self._addBuffer[start:end]