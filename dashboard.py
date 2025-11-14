"""
Credit Card Spending Dashboard
Simple Streamlit dashboard for Travel & Team Building expenses by vertical
"""

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)

# Page config
st.set_page_config(
    page_title="Credit Card Spending Analysis",
    page_icon="📊",
    layout="wide"
)

# Title
st.title("Credit Card Spending Analysis")
st.subheader("Travel & Team Building Expenses: September vs October")

# Data
travel_data = {
    'Vertical': ['Life Science', 'Manufacturing', 'Corporate', 'Distribution', 
                 'Automotive', 'NAD - Ops Management', 'Financial', 'Aviation',
                 'InSite', 'Other', 'COO', 'MIT'],
    'Sep': [66174, 51407, 114624, 22307, 71070, 23730, 23730, 26273, 19122, 6040, 1803, 1803],
    'Oct': [91745, 34983, 77000, 29638, 40009, 34825, 34825, 19134, 7751, 7543, 1238, 1238]
}

tb_data = {
    'Vertical': ['Life Science', 'Manufacturing', 'Technology', 'Corporate', 'Distribution',
                 'Automotive', 'NAD - Ops Management', 'Financial', 'Aviation', 'InSite',
                 'Other', 'COO', 'Puerto Rico', 'Transitions', 'MIT'],
    'Sep': [19177.14, 23147.97, 12664.13, 25689.60, 10087.20, 11914.82, 15458.50, 
            7031.93, 10277.78, 2863.57, 474.22, 903.23, 335.22, 0.00, 501.34],
    'Oct': [37727.36, 27845.67, 22499.17, 21722.44, 15773.18, 10901.07, 10740.03,
            8607.75, 5792.81, 1123.72, 1074.82, 84.92, 25.02, 0.00, 0.00]
}

travel_df = pd.DataFrame(travel_data)
travel_df['Change ($)'] = travel_df['Oct'] - travel_df['Sep']
travel_df['Change (%)'] = ((travel_df['Oct'] - travel_df['Sep']) / travel_df['Sep'] * 100).round(2)
travel_df['Is Down'] = travel_df['Change ($)'] < 0

tb_df = pd.DataFrame(tb_data)
tb_df['Change ($)'] = tb_df['Oct'] - tb_df['Sep']
tb_df['Change (%)'] = ((tb_df['Oct'] - tb_df['Sep']) / tb_df['Sep'].replace(0, np.nan) * 100).round(2)
tb_df['Change (%)'] = tb_df['Change (%)'].fillna(0)
tb_df['Is Down'] = tb_df['Change ($)'] < 0

# Sidebar filters
st.sidebar.header("🔍 Filters")

# Get all unique verticals from both datasets
all_verticals = sorted(set(travel_df['Vertical'].tolist() + tb_df['Vertical'].tolist()))

# Select All checkbox
select_all = st.sidebar.checkbox("Select All", value=True, key="select_all")

if select_all:
    selected_verticals = all_verticals
    # Show selected verticals in faded state
    st.sidebar.markdown("**Selected Verticals:**")
    st.sidebar.markdown(
        '<div style="opacity: 0.6; font-size: 0.9em;">' + 
        '<br>'.join([f'✓ {v}' for v in all_verticals]) + 
        '</div>',
        unsafe_allow_html=True
    )
else:
    selected_verticals = []
    st.sidebar.write("**Select Verticals:**")
    for vertical in all_verticals:
        if st.sidebar.checkbox(vertical, value=False, key=f"vertical_{vertical}"):
            selected_verticals.append(vertical)

# Filter data
if selected_verticals:
    travel_filtered = travel_df[travel_df['Vertical'].isin(selected_verticals)].copy()
    tb_filtered = tb_df[tb_df['Vertical'].isin(selected_verticals)].copy()
else:
    travel_filtered = travel_df.copy()
    tb_filtered = tb_df.copy()

# Summary metrics
col1, col2, col3, col4 = st.columns(4)

total_travel_savings = travel_filtered[travel_filtered['Is Down']]['Change ($)'].sum() * -1
total_tb_savings = tb_filtered[tb_filtered['Is Down']]['Change ($)'].sum() * -1

with col1:
    st.metric("Travel Savings", f"${total_travel_savings:,.0f}")
with col2:
    st.metric("Team Building Savings", f"${total_tb_savings:,.0f}")
with col3:
    st.metric("Total Savings", f"${total_travel_savings + total_tb_savings:,.0f}")
with col4:
    travel_decreased = len(travel_filtered[travel_filtered['Is Down']])
    tb_decreased = len(tb_filtered[tb_filtered['Is Down']])
    st.metric("Verticals with Decreases", f"{travel_decreased + tb_decreased}")

# Tabs for different views
tab1, tab2, tab3 = st.tabs(["📈 Travel Expenses", "🎯 Team Building", "📊 Combined View"])

# Travel Expenses Tab
with tab1:
    st.header("Travel Expenses by Vertical")
    
    if len(travel_filtered) > 0:
        # Bar chart
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
        
        # Sep vs Oct comparison
        travel_sorted = travel_filtered.sort_values('Oct', ascending=False)
        x = range(len(travel_sorted))
        width = 0.35
        
        ax1.bar([i - width/2 for i in x], travel_sorted['Sep'], 
                width, label='Sep', color='#3498db', alpha=0.8)
        ax1.bar([i + width/2 for i in x], travel_sorted['Oct'], 
                width, label='Oct', color='#e74c3c', alpha=0.8)
        ax1.set_xlabel('Vertical', fontsize=10, fontweight='bold')
        ax1.set_ylabel('Amount ($)', fontsize=10, fontweight='bold')
        ax1.set_title('Travel Expenses: Sep vs Oct', fontsize=12, fontweight='bold')
        ax1.set_xticks(x)
        ax1.set_xticklabels(travel_sorted['Vertical'], rotation=45, ha='right', fontsize=9)
        ax1.legend()
        ax1.grid(axis='y', alpha=0.3)
        ax1.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x/1000:.0f}K'))
        
        # Change chart
        colors = ['#2ecc71' if x < 0 else '#e74c3c' for x in travel_sorted['Change ($)']]
        ax2.barh(range(len(travel_sorted)), travel_sorted['Change ($)'], color=colors, alpha=0.7)
        ax2.set_yticks(range(len(travel_sorted)))
        ax2.set_yticklabels(travel_sorted['Vertical'], fontsize=9)
        ax2.set_xlabel('Change ($)', fontsize=10, fontweight='bold')
        ax2.set_title('Change from Sep to Oct', fontsize=12, fontweight='bold')
        ax2.axvline(x=0, color='black', linestyle='--', linewidth=0.8)
        ax2.grid(axis='x', alpha=0.3)
        ax2.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x/1000:.0f}K'))
        
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()
        
        # Data table
        st.subheader("Data Table")
        display_df = travel_filtered[['Vertical', 'Sep', 'Oct', 'Change ($)', 'Change (%)', 'Is Down']].copy()
        display_df.columns = ['Vertical', 'September', 'October', 'Change ($)', 'Change (%)', 'Decreased']
        display_df = display_df.sort_values('October', ascending=False)
        display_df['September'] = display_df['September'].apply(lambda x: f"${x:,.2f}")
        display_df['October'] = display_df['October'].apply(lambda x: f"${x:,.2f}")
        display_df['Change ($)'] = display_df['Change ($)'].apply(lambda x: f"${x:,.2f}")
        display_df['Change (%)'] = display_df['Change (%)'].apply(lambda x: f"{x:.1f}%")
        st.dataframe(display_df, use_container_width=True, hide_index=True)
    else:
        st.info("No data available for selected verticals")

# Team Building Tab
with tab2:
    st.header("Team Building Expenses by Vertical")
    
    if len(tb_filtered) > 0:
        # Bar chart
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
        
        # Sep vs Oct comparison
        tb_sorted = tb_filtered.sort_values('Oct', ascending=False)
        x = range(len(tb_sorted))
        width = 0.35
        
        ax1.bar([i - width/2 for i in x], tb_sorted['Sep'], 
                width, label='Sep', color='#3498db', alpha=0.8)
        ax1.bar([i + width/2 for i in x], tb_sorted['Oct'], 
                width, label='Oct', color='#e74c3c', alpha=0.8)
        ax1.set_xlabel('Vertical', fontsize=10, fontweight='bold')
        ax1.set_ylabel('Amount ($)', fontsize=10, fontweight='bold')
        ax1.set_title('Team Building Expenses: Sep vs Oct', fontsize=12, fontweight='bold')
        ax1.set_xticks(x)
        ax1.set_xticklabels(tb_sorted['Vertical'], rotation=45, ha='right', fontsize=9)
        ax1.legend()
        ax1.grid(axis='y', alpha=0.3)
        ax1.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x/1000:.0f}K'))
        
        # Change chart
        colors = ['#2ecc71' if x < 0 else '#e74c3c' for x in tb_sorted['Change ($)']]
        ax2.barh(range(len(tb_sorted)), tb_sorted['Change ($)'], color=colors, alpha=0.7)
        ax2.set_yticks(range(len(tb_sorted)))
        ax2.set_yticklabels(tb_sorted['Vertical'], fontsize=9)
        ax2.set_xlabel('Change ($)', fontsize=10, fontweight='bold')
        ax2.set_title('Change from Sep to Oct', fontsize=12, fontweight='bold')
        ax2.axvline(x=0, color='black', linestyle='--', linewidth=0.8)
        ax2.grid(axis='x', alpha=0.3)
        ax2.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x/1000:.0f}K'))
        
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()
        
        # Data table
        st.subheader("Data Table")
        display_df = tb_filtered[['Vertical', 'Sep', 'Oct', 'Change ($)', 'Change (%)', 'Is Down']].copy()
        display_df.columns = ['Vertical', 'September', 'October', 'Change ($)', 'Change (%)', 'Decreased']
        display_df = display_df.sort_values('October', ascending=False)
        display_df['September'] = display_df['September'].apply(lambda x: f"${x:,.2f}")
        display_df['October'] = display_df['October'].apply(lambda x: f"${x:,.2f}")
        display_df['Change ($)'] = display_df['Change ($)'].apply(lambda x: f"${x:,.2f}")
        display_df['Change (%)'] = display_df['Change (%)'].apply(lambda x: f"{x:.1f}%")
        st.dataframe(display_df, use_container_width=True, hide_index=True)
    else:
        st.info("No data available for selected verticals")

# Combined View Tab
with tab3:
    st.header("Combined View")
    
    # Merge data for combined view
    combined = pd.merge(
        travel_filtered[['Vertical', 'Sep', 'Oct', 'Change ($)']].rename(columns={
            'Sep': 'Travel_Sep', 'Oct': 'Travel_Oct', 'Change ($)': 'Travel_Change'
        }),
        tb_filtered[['Vertical', 'Sep', 'Oct', 'Change ($)']].rename(columns={
            'Sep': 'TB_Sep', 'Oct': 'TB_Oct', 'Change ($)': 'TB_Change'
        }),
        on='Vertical',
        how='outer'
    ).fillna(0)
    
    combined['Total_Sep'] = combined['Travel_Sep'] + combined['TB_Sep']
    combined['Total_Oct'] = combined['Travel_Oct'] + combined['TB_Oct']
    combined['Total_Change'] = combined['Total_Oct'] - combined['Total_Sep']
    
    if len(combined) > 0:
        # Combined chart
        fig, ax = plt.subplots(figsize=(14, 8))
        
        combined_sorted = combined.sort_values('Total_Oct', ascending=False)
        x = range(len(combined_sorted))
        width = 0.35
        
        ax.bar([i - width/2 for i in x], combined_sorted['Total_Sep'], 
               width, label='Sep', color='#3498db', alpha=0.8)
        ax.bar([i + width/2 for i in x], combined_sorted['Total_Oct'], 
               width, label='Oct', color='#e74c3c', alpha=0.8)
        ax.set_xlabel('Vertical', fontsize=11, fontweight='bold')
        ax.set_ylabel('Amount ($)', fontsize=11, fontweight='bold')
        ax.set_title('Combined Travel & Team Building Expenses: Sep vs Oct', fontsize=13, fontweight='bold')
        ax.set_xticks(x)
        ax.set_xticklabels(combined_sorted['Vertical'], rotation=45, ha='right', fontsize=9)
        ax.legend()
        ax.grid(axis='y', alpha=0.3)
        ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x/1000:.0f}K'))
        
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()
        
        # Combined data table
        st.subheader("Combined Data Table")
        display_df = combined[['Vertical', 'Travel_Sep', 'Travel_Oct', 'TB_Sep', 'TB_Oct', 'Total_Sep', 'Total_Oct', 'Total_Change']].copy()
        display_df.columns = ['Vertical', 'Travel Sep', 'Travel Oct', 'TB Sep', 'TB Oct', 'Total Sep', 'Total Oct', 'Total Change']
        display_df = display_df.sort_values('Total Oct', ascending=False)
        for col in display_df.columns[1:]:
            display_df[col] = display_df[col].apply(lambda x: f"${x:,.2f}")
        st.dataframe(display_df, use_container_width=True, hide_index=True)
    else:
        st.info("No data available for selected verticals")

# Footer
st.markdown("---")
st.caption("Credit Card Spending Analysis - September vs October 2025")

