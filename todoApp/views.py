from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ParseError, NotFound
from .models import Todo, User
from .serializers import TodoSerializer
# Create your views here.
class Todos(APIView):
    def get_user(self, user_id):
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise NotFound("유저를 찾을 수 없습니다.")
        return user
    
    # 투두리스트 전체 조회
    def get(self, request, user_id):
        user = self.get_user(user_id)
        todos = Todo.objects.filter(user=user)

        month = request.query_params.get("month")
        day = request.query_params.get("day")

        if month is not None and day is not None:
            try:
                month = int(month)
                day = int(day)
                todos = todos.filter(date__month=month, date__day=day)
            except ValueError:
                raise ParseError("month와 day는 정수여야 합니다.")

        sort_by = request.query_params.get('sort_by', 'created_at')
        if sort_by not in ['created_at', 'updated_at']:
            sort_by = 'created_at'

        todos = todos.order_by(sort_by)

        serializer = TodoSerializer(todos, many=True)
        return Response(serializer.data)

    def post(self, request, user_id):
        user = self.get_user(user_id)
        serializer = TodoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=user)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

class TodoDetail(APIView):
    def get_user(self, user_id):
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise NotFound("유저를 찾을 수 없습니다.")
        return user

    def get(self, request, user_id, todo_id):
        user = self.get_user(user_id)
        try:
            todo = Todo.objects.get(id=todo_id, user=user)
        except Todo.DoesNotExist:
            raise NotFound("해당 투두를 찾을 수 없습니다.")
        serializer = TodoSerializer(todo)
        return Response(serializer.data)

    def patch(self, request, user_id, todo_id):
        user = self.get_user(user_id)
        try:
            todo = Todo.objects.get(id=todo_id, user=user)
        except Todo.DoesNotExist:
            raise NotFound("해당 투두를 찾을 수 없습니다.")
        serializer = TodoSerializer(todo, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, user_id, todo_id):
        user = self.get_user(user_id)
        try:
            todo = Todo.objects.get(id=todo_id, user=user)
        except Todo.DoesNotExist:
            raise NotFound("해당 투두를 찾을 수 없습니다.")
        todo.delete()
        return Response({"message": "삭제되었습니다."}, status=204)

class TodoCheck(APIView):
    def get_user(self, user_id):
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise NotFound("유저를 찾을 수 없습니다.")

    def get(self, request, user_id, todo_id):
        user = self.get_user(user_id)
        try:
            todo = Todo.objects.get(id=todo_id, user=user)
        except Todo.DoesNotExist:
            raise NotFound("해당 투두를 찾을 수 없습니다.")
        
        serializer = TodoSerializer(todo)
        return Response(serializer.data)

    def patch(self, request, user_id, todo_id):
        user = self.get_user(user_id)
        try:
            todo = Todo.objects.get(id=todo_id, user=user)
        except Todo.DoesNotExist:
            raise NotFound("해당 투두를 찾을 수 없습니다.")

        is_checked = request.data.get('is_checked')
        if is_checked is None:
            raise ParseError("is_checked 필드가 필요합니다.")

        todo.is_checked = bool(is_checked)
        todo.save()
        serializer = TodoSerializer(todo)
        return Response(serializer.data)

class TodoReview(APIView):
    def get_user(self, user_id):
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise NotFound("유저를 찾을 수 없습니다.")

    def get(self, request, user_id, todo_id):
        user = self.get_user(user_id)
        try:
            todo = Todo.objects.get(id=todo_id, user=user)
        except Todo.DoesNotExist:
            raise NotFound("해당 투두를 찾을 수 없습니다.")
        serializer = TodoSerializer(todo)
        return Response(serializer.data)

    def patch(self, request, user_id, todo_id):
        user = self.get_user(user_id)
        try:
            todo = Todo.objects.get(id=todo_id, user=user)
        except Todo.DoesNotExist:
            raise NotFound("해당 투두를 찾을 수 없습니다.")

        review = request.data.get("review")
        if review is None:
            raise ParseError("리뷰 내용이 필요합니다.")

        todo.review = review
        todo.save()
        serializer = TodoSerializer(todo)
        return Response(serializer.data)
    
    def delete(self, request, user_id, todo_id):
        user = self.get_user(user_id)
        try:
            todo = Todo.objects.get(id=todo_id, user=user)
        except Todo.DoesNotExist:
            raise NotFound("해당 투두를 찾을 수 없습니다.")
        todo.review = "" 
        todo.save()
        return Response({"message": "삭제되었습니다."}, status=204)