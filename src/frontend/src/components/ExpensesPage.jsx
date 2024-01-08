import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Navigate } from 'react-router-dom';
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import '../css/ExpensesPageAdd.css'

const ExpensesPage = () => {
  const [expenses, setExpenses] = useState([]);
  const [error, setError] = useState(null);
  const [showModal, setShowModal] = useState(false); // состояние для управления видимостью модального окна
  const [newExpenseData, setNewExpenseData] = useState({
    name: '',
    amount: 0,
    category_id: 0
  });
  const [editMode, setEditMode] = useState(false); // состояние для переключения в режим редактирования
  const [editedExpenseId, setEditedExpenseId] = useState(null); // ID выбранной записи для редактирования
  const [editedExpenseData, setEditedExpenseData] = useState({
    name: '',
    amount: 0,
    category_id: 0
  });
  const [redirectToLogin, setRedirectToLogin] = useState(false);

  const fetchExpenses = async () => {
    try {
      const token = localStorage.getItem('token');
      const response = await axios.get('http://127.0.0.1:8000/expenses/', {
        headers: {
          'accept': 'application/json',
          'Authorization': `Bearer ${token}`
        }
      });
      setExpenses(response.data);
    } catch (error) {
      if (error.response.status === 401) {
        setRedirectToLogin(true);
      }
      setError(error.message);
    }
  };

  useEffect(() => {
    fetchExpenses();
  }, []);

  const handleAddExpense = async (event) => {
    event.preventDefault();

    if (newExpenseData.name.length < 2) {
      toast.error("Описание должно содержать более двух символов");
      return;
    }

    if (newExpenseData.amount <= 0) {
      toast.error("Сумма должна быть больше нуля");
      return;
    }

    try {
      const token = localStorage.getItem('token');
      await axios.post('http://127.0.0.1:8000/expenses/', newExpenseData, {
        headers: {
          'accept': 'application/json',
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      });
      fetchExpenses(); // обновляем список после добавления
      setShowModal(false); // скрываем модальное окно
      toast.success("Запись добавлена!", {
        position: toast.POSITION.BOTTOM_RIGHT,
      });
    } catch (error) {
      setError(error.message);
      localStorage.removeItem('token');
    }
  };

  const handleChange = (e) => {
    const { name, value } = e.target;

    setNewExpenseData({
      ...newExpenseData,
      [name]: value
    });
  };

  const handleEditClick = (expenseId, name, amount, categoryId) => {
    setEditMode(true);
    setEditedExpenseId(expenseId);
    setEditedExpenseData({ name, amount, category_id: categoryId });
  };

  const handleSaveEdit = async () => {
    try {
      const token = localStorage.getItem('token');
      const response = await axios.patch(`http://127.0.0.1:8000/expenses/${editedExpenseId}`, editedExpenseData, {
        headers: {
          'accept': 'application/json',
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      });
      fetchExpenses();
      setEditMode(false);
      setEditedExpenseId(null);
    } catch (error) {
      console.log(error.response.status);
      if (error.response.status === 422) {
        toast.error("Запись не изменена", {
          position: toast.POSITION.BOTTOM_RIGHT,
        });
      } else if (error.response.status === 401) {
        setRedirectToLogin(true);
      }
      // localStorage.removeItem('token');
    }
  };

  return (
    <div>
      {redirectToLogin && <Navigate to='/login' />}
      <h1>Затраты</h1>
      <button onClick={() => setShowModal(true)}>Добавить запись</button>
      {showModal && (
        <div className='modal-background'>
          <div className="modal-content">
            <h2>Добавить запись</h2>
            <form onSubmit={handleAddExpense}>
              <div>
                <label>
                  Описание:
                  <input
                    type="text"
                    name="name"
                    value={newExpenseData.name}
                    onChange={handleChange}
                  />
                </label>
              </div>
              <div>
                <label>
                  Сумма:
                  <input
                    type="number"
                    name="amount"
                    value={newExpenseData.amount}
                    onChange={handleChange}
                  />
                </label>
              </div>
              <div>
                <label>
                  ID категории:
                  <input
                    type="number"
                    name="category_id"
                    value={newExpenseData.category_id}
                    onChange={handleChange}
                  />
                </label>
              </div>
              <div>
                <button type="submit">Добавить</button>
                <ToastContainer />
              </div>
              <button type="button" onClick={() => setShowModal(false)}>Отмена</button>
            </form>
          </div>
        </div>
      )}
      <table>
        <thead>
          <tr>
            <td>Описание</td>
            <td>Сумма</td>
            <td>Изменить</td> {/* Новая колонка для кнопки изменения */}
          </tr>
        </thead>
        <tbody>
          {expenses.map((expense) => (
            <tr key={expense.id}>
              <td>
                {editMode && editedExpenseId === expense.id ? (
                  <input
                    type="text"
                    value={editedExpenseData.name}
                    onChange={(e) => setEditedExpenseData({ ...editedExpenseData, name: e.target.value })}
                  />
                ) : (
                  expense.name
                )}
              </td>
              <td>
                {editMode && editedExpenseId === expense.id ? (
                  <input
                    type="number"
                    value={editedExpenseData.amount}
                    onChange={(e) => setEditedExpenseData({ ...editedExpenseData, amount: e.target.value })}
                  />
                ) : (
                  expense.amount
                )}
              </td>
              <td>
                {editMode && editedExpenseId === expense.id ? (
                  <button onClick={handleSaveEdit}>Сохранить</button>
                ) : (
                  <button onClick={() => handleEditClick(expense.id, expense.name, expense.amount, expense.category_id)}>
                    Изменить
                  </button>
                )}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default ExpensesPage;