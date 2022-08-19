#!/usr/bin/env python
# coding: utf-8

# # Datapane template

# In[1]:


import datapane as dp
import numpy as np
import pandas as pd
import platypus as plat
import plotly.express as px
import plotly.graph_objects as go


# ## Build blocks for markdown placeholders
# 
# We've duplicated the code cells from our source notebook (`assets/article.ipynb`).
# 
# Let's go through and turn what would have been _output cells_ into Datapane objects. We'll create them inline after each placeholder, e.g. `{{ placeholder_name }}`, and give the variables corresponding names to keep things simple.

# In[2]:


problem = plat.ZDT1()
D = 30
N = 50


# In[3]:


solutions = []

for i in range(N):
    solution = plat.Solution(problem)
    solution.variables = np.random.rand(D)
    solution.evaluate()
    solutions.append(solution)


# In[4]:


print(f"Design variables: {solutions[0].variables}")
print(f"Objective values: {solutions[0].objectives}")


# {{text_variables_and_objectives}}

# In[5]:


text_variables_and_objectives = dp.Text(
    f"""Design variables:\n {solutions[0].variables}

Objective values:\n {solutions[0].objectives}
"""
)


# In[6]:


plat.nondominated_sort(solutions)


# In[7]:


solutions[0].rank


# {{text_solution_rank}}

# In[8]:


text_solution_rank = dp.Text(f"{solutions[0].rank}")


# In[9]:


solutions_df = pd.DataFrame(index=range(N), columns=["f1", "f2", "front_rank"])
solutions_df.head()


# {{datatable_solutions_initialised}}

# In[10]:


datatable_solutions_initialised = dp.Table(solutions_df.head())


# In[11]:


for i in range(N):
    solutions_df.loc[i].f1 = solutions[i].objectives[0]
    solutions_df.loc[i].f2 = solutions[i].objectives[1]
    solutions_df.loc[i].front_rank = solutions[i].rank

solutions_df.head()


# {{datatable_solutions_evaluated}}

# In[12]:


datatable_solutions_evaluated = dp.DataTable(solutions_df)


# In[13]:


fig = go.Figure(layout=dict(xaxis=dict(title="f1"), yaxis=dict(title="f2")))

fig.add_scatter(x=solutions_df.f1, y=solutions_df.f2, mode="markers")

fig.show()


# {{plot_objective_space}}

# In[14]:


plot_objective_space = dp.Plot(fig)


# In[15]:


solutions_df.front_rank.nunique()


# {{text_unique_fronts}}

# In[16]:


text_unique_fronts = dp.Text(f"{solutions_df.front_rank.nunique()}")


# We will then need to produce a sorted vector containing the rank of each front.

# In[17]:


fronts = sorted(solutions_df.front_rank.unique())
print(fronts)


# {{text_fronts}}

# In[18]:


text_fronts = dp.Text(f"{fronts}")


# In[19]:


fig = go.Figure(layout=dict(xaxis=dict(title="f1"), yaxis=dict(title="f2")))

for front in fronts:
    front_solutions_df = solutions_df.loc[solutions_df.front_rank == front]
    fig.add_scatter(
        x=front_solutions_df.f1,
        y=front_solutions_df.f2,
        name=f"front {front}",
        mode="markers",
        marker=dict(color=px.colors.qualitative.Plotly[front], size=10 ),    )

fig.show()


# {{plot_solutions_ranked}}

# In[20]:


plot_solutions_ranked = dp.Plot(fig)


# In[21]:


fig = px.scatter(solutions_df, x="f1", y="f2", color="front_rank")
fig.update_traces(marker=dict(size=12))
fig


# {{plot_solutions_ranked_px}}

# In[22]:


plot_solutions_ranked_px = dp.Plot(fig)


# ## Build header blocks

# In[23]:


fig = go.Figure()

for front in fronts:
    front_solutions_df = solutions_df.loc[solutions_df.front_rank == front]
    fig.add_scatter(
        x=front_solutions_df.f1,
        y=front_solutions_df.f2,
        name=f"front {front}",
        mode="markers",
        marker=dict(
            color=px.colors.qualitative.Plotly[front],
            size=20,
            line=dict(color="#444444", width=2),
        ),
    )

fig.update_layout(
    template="seaborn", height=100, margin=dict(l=0, r=0, t=0, b=0), showlegend=False
)
fig.update_xaxes(visible=False)
fig.update_yaxes(visible=False)

banner_block = dp.Plot(fig)


# ## Build report

# In[24]:


report = dp.Report(
    banner_block,
    dp.Text("# Non-Dominated Sorting"),
    dp.Text(file="assets/article.md").format(
        # placeholders in our articles.md will be replaced with Datapane objects.
        text_variables_and_objectives=text_variables_and_objectives,
        text_solution_rank=text_solution_rank,
        datatable_solutions_initialised=datatable_solutions_initialised,
        datatable_solutions_evaluated=datatable_solutions_evaluated,
        plot_objective_space=plot_objective_space,
        text_unique_fronts=text_unique_fronts,
        text_fronts=text_fronts,
        plot_solutions_ranked=plot_solutions_ranked,
        plot_solutions_ranked_px=plot_solutions_ranked_px,
    ),
)

report.save(path="template.html", open=True)

