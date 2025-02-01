from BankTransactionsDashboard import *
from BeRebelDashboard import *
from SalaryDashboard import *

# Define file paths
csv_paths = {
    "Salary": get_csv_path(
        "../backend/resources/output_data/salary/salary_history.csv"
    ),
    "Bank Transactions": get_csv_path(
        "../backend/resources/output_data/bank_transactions/ing/bank_transactions_history.csv"
    ),
    "BeRebel": get_csv_path(
        "../backend/resources/output_data/berebel/berebel_history.csv"
    ),
}
# Load data
salary_data = load_data(csv_paths["Salary"])
bank_transactions_data = load_data(csv_paths["Bank Transactions"])
berebel_data = load_data(csv_paths["BeRebel"])

# Sidebar navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Select Page", csv_paths.keys())

# Display selected dashboard
if page == "Salary" and salary_data is not None:
    salary_dashboard(salary_data)
elif page == "Bank Transactions" and bank_transactions_data is not None:
    bank_transactions_charts(bank_transactions_data)
elif page == "BeRebel" and berebel_data is not None:
    berebel_dashboard(berebel_data)
else:
    st.warning(
        f"No data available for {page}. Check the file path or upload a valid CSV."
    )
