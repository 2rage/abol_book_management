import grpc
from concurrent import futures
from grpc_reflection.v1alpha import reflection
from grpc_service import books_pb2, books_pb2_grpc
from sqlalchemy.orm import Session
from web_app.dependencies import get_db
from web_app.models import Book


class BookServiceServicer(books_pb2_grpc.BookServiceServicer):
    def __init__(self, db_session):
        self.db_session = db_session

    def GetBook(self, request, context):
        db = next(self.db_session())
        try:
            book = db.query(Book).filter(Book.id == request.id).first()
            if book is None:
                context.abort(grpc.StatusCode.NOT_FOUND, "Book not found")
            return books_pb2.BookResponse(
                id=book.id,
                title=book.title,
                author=book.author,
                publication_date=str(book.publication_date),
            )
        finally:
            db.close()

    def ListBooks(self, request, context):
        db = next(self.db_session())
        try:
            books = db.query(Book).all()
            return books_pb2.BookList(
                books=[
                    books_pb2.BookResponse(
                        id=book.id,
                        title=book.title,
                        author=book.author,
                        publication_date=str(book.publication_date),
                    )
                    for book in books
                ]
            )
        finally:
            db.close()


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    books_pb2_grpc.add_BookServiceServicer_to_server(
        BookServiceServicer(get_db), server
    )

    SERVICE_NAMES = (
        books_pb2.DESCRIPTOR.services_by_name["BookService"].full_name,
        reflection.SERVICE_NAME,
    )
    reflection.enable_server_reflection(SERVICE_NAMES, server)

    server.add_insecure_port("[::]:50051")
    server.start()
    print("gRPC server started on port 50051")
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
