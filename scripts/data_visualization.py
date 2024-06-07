import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from fpdf import FPDF
import os

# Usar caminho absoluto para o arquivo
file_path = os.path.abspath(os.path.join('data', 'cleaned_Amazon_Sale_Report.csv'))

# Verifique se o arquivo existe
if not os.path.exists(file_path):
    raise FileNotFoundError(f"The file {file_path} does not exist.")
else:
    print(f"File found: {file_path}")

# Carregar dados limpos
df = pd.read_csv(file_path)
print("Data loaded successfully.")

# Configurações de Estilo
sns.set(style='whitegrid')
plt.style.use('fivethirtyeight')

# Garantir que o diretório 'reports' exista
reports_dir = os.path.abspath(os.path.join('reports'))
os.makedirs(reports_dir, exist_ok=True)

# Função para criar gráficos e salvar em arquivos de imagem
def create_visualizations(df):
    print("Creating visualizations...")

    # Distribuição de Vendas por Estado
    plt.figure(figsize=(10, 20))
    sns.countplot(y='ship-state', data=df, order=df['ship-state'].value_counts().index, palette="viridis", hue='ship-state', dodge=False)
    plt.title('Distribuição de Vendas por Estado')
    plt.xlabel('Contagem')
    plt.ylabel('Estado')
    plt.tight_layout()
    plt.savefig(os.path.join(reports_dir, 'sales_by_state.png'))
    plt.close()
    print("Saved sales_by_state.png")

    # Vendas ao Longo do Tempo
    df['Date'] = pd.to_datetime(df['Date'])
    df.set_index('Date', inplace=True)
    monthly_sales = df.resample('MS').sum()['TotalPrice']
    plt.figure(figsize=(14, 7))
    sns.lineplot(data=monthly_sales, marker="o", color="b")
    plt.title('Vendas Mensais')
    plt.xlabel('Mês')
    plt.ylabel('Total de Vendas')
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(os.path.join(reports_dir, 'monthly_sales.png'))
    plt.close()
    print("Saved monthly_sales.png")

    # Produtos Mais Vendidos
    top_products = df.groupby('SKU')['Qty'].sum().sort_values(ascending=False).head(10)
    plt.figure(figsize=(14, 7))
    sns.barplot(x=top_products.values, y=top_products.index, palette="viridis")
    plt.title('Top 10 Produtos Mais Vendidos')
    plt.xlabel('Quantidade Vendida')
    plt.ylabel('Produto')
    plt.tight_layout()
    plt.savefig(os.path.join(reports_dir, 'top_products.png'))
    plt.close()
    print("Saved top_products.png")

    # Receita Total por Estado
    state_revenue = df.groupby('ship-state')['TotalPrice'].sum().sort_values(ascending=False)
    plt.figure(figsize=(14, 20))
    sns.barplot(x=state_revenue.values, y=state_revenue.index, palette="viridis")
    plt.title('Receita Total por Estado')
    plt.xlabel('Receita Total')
    plt.ylabel('Estado')
    plt.tight_layout()
    plt.savefig(os.path.join(reports_dir, 'revenue_by_state.png'))
    plt.close()
    print("Saved revenue_by_state.png")

    # Receita Média por Produto
    average_revenue_per_product = df.groupby('SKU')['TotalPrice'].mean().sort_values(ascending=False).head(10)
    plt.figure(figsize=(14, 7))
    sns.barplot(x=average_revenue_per_product.values, y=average_revenue_per_product.index, palette="viridis")
    plt.title('Receita Média por Produto')
    plt.xlabel('Receita Média')
    plt.ylabel('Produto')
    plt.tight_layout()
    plt.savefig(os.path.join(reports_dir, 'average_revenue_per_product.png'))
    plt.close()
    print("Saved average_revenue_per_product.png")

# Função para criar um relatório PDF
def create_pdf_report():
    print("Creating PDF report...")
    pdf = FPDF()
    pdf.add_page()

    # Título do Relatório
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(200, 10, 'E-commerce Data Analysis Report', ln=True, align='C')

    # Introdução
    pdf.set_font('Arial', '', 12)
    pdf.multi_cell(0, 10, "This report provides an analysis of the e-commerce sales data, "
                          "including sales distribution by state, monthly sales trends, "
                          "the top 10 best-selling products, total revenue by state, and "
                          "average revenue per product.")
    pdf.ln(10)

    # Distribuição de Vendas por Estado
    pdf.set_font('Arial', 'B', 14)
    pdf.cell(200, 10, '1. Distribution of Sales by State', ln=True)
    pdf.set_font('Arial', '', 12)
    pdf.multi_cell(0, 10, 'The chart below shows the distribution of sales across different states.')
    pdf.ln(5)
    pdf.image(os.path.join(reports_dir, 'sales_by_state.png'), x=10, w=190)
    pdf.ln(105)

    # Vendas ao Longo do Tempo
    pdf.add_page()
    pdf.set_font('Arial', 'B', 14)
    pdf.cell(200, 10, '2. Monthly Sales Trends', ln=True)
    pdf.set_font('Arial', '', 12)
    pdf.multi_cell(0, 10, 'The chart below shows the monthly sales trends over time. Identifying peak sales periods can help in planning marketing strategies and inventory management.')
    pdf.ln(5)
    pdf.image(os.path.join(reports_dir, 'monthly_sales.png'), x=10, w=190)
    pdf.ln(85)

    # Top 10 Produtos Mais Vendidos
    pdf.add_page()
    pdf.set_font('Arial', 'B', 14)
    pdf.cell(200, 10, '3. Top 10 Best-Selling Products', ln=True)
    pdf.set_font('Arial', '', 12)
    pdf.multi_cell(0, 10, 'The chart below lists the top 10 best-selling products based on the quantity sold. Understanding which products are most popular can help in focusing marketing efforts and optimizing stock levels.')
    pdf.ln(5)
    pdf.image(os.path.join(reports_dir, 'top_products.png'), x=10, w=190)
    pdf.ln(85)

    # Receita Total por Estado
    pdf.add_page()
    pdf.set_font('Arial', 'B', 14)
    pdf.cell(200, 10, '4. Total Revenue by State', ln=True)
    pdf.set_font('Arial', '', 12)
    pdf.multi_cell(0, 10, 'The chart below shows the total revenue generated in each state. This can help in targeting regions with high revenue for further business opportunities and improving strategies in regions with lower revenue.')
    pdf.ln(5)
    pdf.image(os.path.join(reports_dir, 'revenue_by_state.png'), x=10, w=190)
    pdf.ln(105)

    # Receita Média por Produto
    pdf.add_page()
    pdf.set_font('Arial', 'B', 14)
    pdf.cell(200, 10, '5. Average Revenue per Product', ln=True)
    pdf.set_font('Arial', '', 12)
    pdf.multi_cell(0, 10, 'The chart below shows the average revenue per product. This analysis helps in understanding the profitability of products and making informed decisions on pricing and promotions.')
    pdf.ln(5)
    pdf.image(os.path.join(reports_dir, 'average_revenue_per_product.png'), x=10, w=190)
    pdf.ln(85)

    pdf.output(os.path.join(reports_dir, 'ecommerce_report.pdf'))
    print("PDF report created and saved as ecommerce_report.pdf")

if __name__ == "__main__":
    create_visualizations(df)
    create_pdf_report()
    print("All tasks completed successfully.")