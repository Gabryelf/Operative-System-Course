"""Класс интерфейса. Отвечает только за отображение и взаимодействие с пользователем."""

import tkinter as tk
from tkinter import ttk, messagebox
from typing import Optional
from models import Contact
from service import ContactService


class PhoneBookApp(tk.Tk):
    def __init__(self, service: ContactService):
        super().__init__()
        self._service = service
        self._selected_contact: Optional[Contact] = None

        self.title("Телефонный справочник")
        self.geometry("700x500")

        self._build_ui()
        self._refresh_list()

    def _build_ui(self):
        # --- Верхняя панель: поиск ---
        search_frame = ttk.Frame(self, padding=10)
        search_frame.pack(fill=tk.X)

        ttk.Label(search_frame, text="Поиск:").pack(side=tk.LEFT)
        self._search_var = tk.StringVar()
        search_entry = ttk.Entry(search_frame, textvariable=self._search_var, width=30)
        search_entry.pack(side=tk.LEFT, padx=5)
        ttk.Button(search_frame, text="Найти", command=self._on_search).pack(side=tk.LEFT)
        ttk.Button(search_frame, text="Сбросить", command=self._on_reset).pack(side=tk.LEFT, padx=5)

        # --- Таблица контактов ---
        table_frame = ttk.Frame(self, padding=10)
        table_frame.pack(fill=tk.BOTH, expand=True)

        columns = ("id", "name", "phone")
        self._tree = ttk.Treeview(table_frame, columns=columns, show="headings")
        self._tree.heading("id", text="ID")
        self._tree.heading("name", text="Имя")
        self._tree.heading("phone", text="Телефон")
        self._tree.column("id", width=50, anchor=tk.CENTER)
        self._tree.column("name", width=250)
        self._tree.column("phone", width=150)
        self._tree.pack(fill=tk.BOTH, expand=True)

        self._tree.bind("<<TreeviewSelect>>", self._on_select)

        # --- Форма ввода ---
        form_frame = ttk.LabelFrame(self, text="Контакт", padding=10)
        form_frame.pack(fill=tk.X, padx=10, pady=5)

        ttk.Label(form_frame, text="Имя:").grid(row=0, column=0, sticky=tk.W)
        self._name_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self._name_var, width=30).grid(row=0, column=1, padx=5, pady=2)

        ttk.Label(form_frame, text="Телефон:").grid(row=0, column=2, sticky=tk.W)
        self._phone_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self._phone_var, width=20).grid(row=0, column=3, padx=5, pady=2)

        # --- Кнопки действий ---
        btn_frame = ttk.Frame(self, padding=10)
        btn_frame.pack(fill=tk.X)

        ttk.Button(btn_frame, text="Добавить", command=self._on_add).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_frame, text="Изменить", command=self._on_update).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_frame, text="Удалить", command=self._on_delete).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_frame, text="Очистить форму", command=self._clear_form).pack(side=tk.LEFT, padx=2)

    def _refresh_list(self):
        for item in self._tree.get_children():
            self._tree.delete(item)
        for contact in self._service.get_all_contacts():
            self._tree.insert("", tk.END, values=(contact.id, contact.name, contact.phone))

    def _on_search(self):
        query = self._search_var.get()
        for item in self._tree.get_children():
            self._tree.delete(item)
        for contact in self._service.search_contacts(query):
            self._tree.insert("", tk.END, values=(contact.id, contact.name, contact.phone))

    def _on_reset(self):
        self._search_var.set("")
        self._refresh_list()

    def _on_select(self, event):
        selected = self._tree.selection()
        if not selected:
            return
        values = self._tree.item(selected[0], "values")
        self._selected_contact = Contact(id=int(values[0]), name=values[1], phone=values[2])
        self._name_var.set(values[1])
        self._phone_var.set(values[2])

    def _on_add(self):
        self._service.add_contact(self._name_var.get(), self._phone_var.get())
        self._clear_form()
        self._refresh_list()

    def _on_update(self):
        if not self._selected_contact:
            messagebox.showwarning("Внимание", "Выберите контакт для изменения")
            return
        updated = Contact(
            id=self._selected_contact.id,
            name=self._name_var.get(),
            phone=self._phone_var.get()
        )
        self._service.update_contact(updated)
        self._clear_form()
        self._refresh_list()

    def _on_delete(self):
        if not self._selected_contact:
            messagebox.showwarning("Внимание", "Выберите контакт для удаления")
            return
        if not messagebox.askyesno("Подтверждение", f"Удалить контакт '{self._selected_contact.name}'?"):
            return
        self._service.delete_contact(self._selected_contact.id)
        self._clear_form()
        self._refresh_list()

    def _clear_form(self):
        self._selected_contact = None
        self._name_var.set("")
        self._phone_var.set("")
        self._tree.selection_remove(self._tree.selection())
