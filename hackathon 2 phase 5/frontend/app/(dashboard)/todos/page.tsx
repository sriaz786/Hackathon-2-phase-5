"use client";

import { useEffect, useState } from "react";
import { useAuth } from "../../../context/AuthContext";
import api from "../../../lib/api";
import { useRouter } from "next/navigation";

interface Todo {
  id: number;
  title: string;
  description: string | null;
  status: string;
}

export default function TodosPage() {
  const { user, loading, logout } = useAuth();
  const router = useRouter();
  const [todos, setTodos] = useState<Todo[]>([]);
  const [newTodoTitle, setNewTodoTitle] = useState("");
  const [newTodoDesc, setNewTodoDesc] = useState("");
  const [error, setError] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);

  useEffect(() => {
    if (!loading && !user) {
      router.push("/login");
    }
    if (user) {
      fetchTodos();
    }
  }, [user, loading, router]);

  const fetchTodos = async () => {
    try {
      const response = await api.get("/todos");
      setTodos(response.data);
    } catch (err) {
      console.error(err);
      setError("Failed to fetch todos");
    }
  };

  const addTodo = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newTodoTitle.trim()) return;
    setIsSubmitting(true);
    try {
      const response = await api.post("/todos", {
        title: newTodoTitle,
        description: newTodoDesc,
      });
      setTodos([...todos, response.data]);
      setNewTodoTitle("");
      setNewTodoDesc("");
    } catch (err) {
      console.error(err);
      setError("Failed to add todo");
    } finally {
      setIsSubmitting(false);
    }
  };

  const toggleTodo = async (todo: Todo) => {
    try {
      const newStatus = todo.status === "completed" ? "pending" : "completed";
      const response = await api.put(`/todos/${todo.id}`, {
        status: newStatus,
      });
      setTodos(todos.map((t) => (t.id === todo.id ? response.data : t)));
    } catch (err) {
      console.error(err);
      setError("Failed to update todo");
    }
  };

  const deleteTodo = async (id: number) => {
    try {
      await api.delete(`/todos/${id}`);
      setTodos(todos.filter((t) => t.id !== id));
    } catch (err) {
      console.error(err);
      setError("Failed to delete todo");
    }
  };

  if (loading)
    return (
      <div className="flex items-center justify-center min-h-screen bg-gray-50">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600"></div>
      </div>
    );

  if (!user) return null;

  return (
    <div className="min-h-screen bg-gray-50 text-gray-900 font-sans">
      <nav className="bg-white shadow-sm border-b border-gray-200 sticky top-0 z-10">
        <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16 items-center">
            <div className="flex items-center gap-2">
              <div className="bg-indigo-600 h-8 w-8 rounded-lg flex items-center justify-center">
                <span className="text-white font-bold text-lg">T</span>
              </div>
              <h1 className="text-xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-indigo-600 to-purple-600">
                TaskFlow
              </h1>
            </div>
            <div className="flex items-center gap-4">
              <span className="text-sm text-gray-500 hidden sm:inline">
                signed in as{" "}
                <span className="font-medium text-gray-900">{user.email}</span>
              </span>
              <button
                onClick={logout}
                className="px-4 py-2 text-sm font-medium text-red-600 bg-red-50 hover:bg-red-100 rounded-lg transition-colors"
              >
                Logout
              </button>
            </div>
          </div>
        </div>
      </nav>

      <main className="max-w-5xl mx-auto p-4 sm:p-6 lg:p-8 mt-4">
        {error && (
          <div className="bg-red-50 border-l-4 border-red-500 p-4 mb-6 rounded-r shadow-sm">
            <p className="text-sm text-red-700">{error}</p>
          </div>
        )}

        <div className="bg-white rounded-2xl shadow-sm border border-gray-200 p-6 mb-8 transition-shadow hover:shadow-md">
          <h2 className="text-lg font-semibold text-gray-800 mb-4">
            Add New Task
          </h2>
          <form onSubmit={addTodo} className="space-y-4">
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
              <div className="md:col-span-4">
                <input
                  type="text"
                  value={newTodoTitle}
                  onChange={(e) => setNewTodoTitle(e.target.value)}
                  className="w-full px-4 py-3 bg-gray-50 border border-gray-200 rounded-xl focus:bg-white focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition-all outline-none text-gray-900 placeholder-gray-400"
                  placeholder="What needs to be done?"
                  required
                />
              </div>
              <div className="md:col-span-4">
                <textarea
                  value={newTodoDesc}
                  onChange={(e) => setNewTodoDesc(e.target.value)}
                  className="w-full px-4 py-3 bg-gray-50 border border-gray-200 rounded-xl focus:bg-white focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition-all outline-none text-gray-900 placeholder-gray-400 min-h-[80px] resize-y"
                  placeholder="Add details (optional)..."
                />
              </div>
            </div>
            <div className="flex justify-end">
              <button
                type="submit"
                disabled={isSubmitting || !newTodoTitle.trim()}
                className="px-6 py-2.5 bg-indigo-600 text-white font-medium rounded-xl hover:bg-indigo-700 active:bg-indigo-800 transition-colors shadow-lg shadow-indigo-200 disabled:opacity-50 disabled:shadow-none"
              >
                {isSubmitting ? "Adding..." : "Add Task"}
              </button>
            </div>
          </form>
        </div>

        <div className="space-y-4">
          <h2 className="text-lg font-semibold text-gray-800 pl-1">My Tasks</h2>
          {todos.length === 0 ? (
            <div className="text-center py-16 bg-white rounded-2xl border border-gray-200 border-dashed">
              <p className="text-gray-400 text-lg">
                No tasks yet. Add one above!
              </p>
            </div>
          ) : (
            <div className="grid grid-cols-1 gap-4">
              {todos.map((todo) => (
                <div
                  key={todo.id}
                  className={`group bg-white p-5 rounded-2xl border transition-all duration-200 hover:shadow-md flex items-start justify-between gap-4 ${
                    todo.status === "completed"
                      ? "border-gray-200 bg-gray-50/50"
                      : "border-gray-200"
                  }`}
                >
                  <div className="flex-1 flex gap-4 min-w-0">
                    <div className="pt-1">
                      <input
                        type="checkbox"
                        checked={todo.status === "completed"}
                        onChange={() => toggleTodo(todo)}
                        className="h-6 w-6 rounded-md border-gray-300 text-indigo-600 focus:ring-indigo-500 cursor-pointer"
                      />
                    </div>
                    <div className="min-w-0 flex-1">
                      <h3
                        className={`text-lg font-medium truncate pr-4 ${
                          todo.status === "completed"
                            ? "line-through text-gray-400"
                            : "text-gray-900"
                        }`}
                      >
                        {todo.title}
                      </h3>
                      {todo.description && (
                        <p
                          className={`mt-1 text-sm ${
                            todo.status === "completed"
                              ? "line-through text-gray-400"
                              : "text-gray-500"
                          }`}
                        >
                          {todo.description}
                        </p>
                      )}
                    </div>
                  </div>
                  <button
                    onClick={() => deleteTodo(todo.id)}
                    className="p-2 text-gray-400 hover:text-red-500 hover:bg-red-50 rounded-lg transition-colors opacity-0 group-hover:opacity-100 focus:opacity-100"
                    title="Delete task"
                  >
                    <svg
                      xmlns="http://www.w3.org/2000/svg"
                      className="h-5 w-5"
                      fill="none"
                      viewBox="0 0 24 24"
                      stroke="currentColor"
                    >
                      <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        strokeWidth={2}
                        d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"
                      />
                    </svg>
                  </button>
                </div>
              ))}
            </div>
          )}
        </div>
      </main>
    </div>
  );
}
