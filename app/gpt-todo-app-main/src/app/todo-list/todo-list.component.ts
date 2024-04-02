import { Component } from '@angular/core';

@Component({
  selector: 'app-todo-list',
  templateUrl: './todo-list.component.html',
  styleUrls: ['./todo-list.component.css']
})
export class TodoListComponent {
  newTodoText = '';
  todos: { todo: string; completed: boolean }[] = [];

  addTodo(todo: string) {
    // console.log(this.newTodoText);
    this.todos.push({ todo: todo, completed: false});
  }

  toggleCompleted(todo: { todo: string; completed: boolean }) {
    todo.completed = !todo.completed;
  }

  deleteTodo(todo: { todo: string; completed: boolean }) {
    this.todos = this.todos.filter((t) => t !== todo);
  }
}
