import os
from BeRebelDashboard import *
from SalaryDashboard import *
from BankTransactionsDashboard import *

# CSV file path in the resources folder
base_path = os.path.abspath(os.path.dirname(__file__))
salary_csv_path = os.path.join(base_path, "../backend/resources/output_data/salary/salary_history.csv")
bank_transactions_ing_csv_path = os.path.join(base_path, "../backend/resources/output_data/bank_transactions/ing/bank_transactions_history.csv")
berebel_csv_path = os.path.join(base_path, "../backend/resources/output_data/berebel/berebel_history.csv")


# Load data
salary_data = load_data(salary_csv_path)
bank_transactions_data = load_data(bank_transactions_ing_csv_path)
berebel_data = load_data(berebel_csv_path)

# Sidebar for navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Select Page", ["Salary Dashboard", "Bank Transactions Dashboard", "BeRebel Dashboard"])

# Display selected page
if salary_data is not None:
    if page == "Salary Dashboard":
        salary_dashboard(salary_data)
    elif page == "Bank Transactions Dashboard":
        bank_transactions_charts(bank_transactions_data)
    elif page == "BeRebel Dashboard":
        berebel_dashboard(berebel_data)
else:
    st.warning(f"Upload a CSV file to start or check the path: Root: {base_path} - Folder: {salary_csv_path}")
