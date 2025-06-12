from crewai import Agent, Task, Crew, Process
from typing import List
from crewai_tools import FileReadTool, CSVSearchTool
from modules.utils import *
from modules.tools import *


class SalesAnalystAgent:
    def __init__(self):
        self.llm = load_llm()
        self.output_dir = "output"
        self.sql_tools = [tables_schema, execute_sql]

    def create_agents(self) -> List[Agent]:
        data_analyst = Agent(
            role='Data Analyst',
            goal='Analyze sales data to answer: {question}',
            backstory="""You are an expert data analyst with extensive experience in sales analysis.
            You excel at identifying patterns, trends, and key metrics in sales data.
            Use the `tables_schema` to understand the metadata for the tables.
            Use the `execute_sql` to execute queries.""",
            verbose=True,
            allow_delegation=True,
            llm=self.llm,
            tools=self.sql_tools,
            cache=True
        )

        sales_strategist = Agent(
            role='Sales Strategist',
            goal='Develop strategic recommendations based on sales analysis for: {question}',
            backstory="""You are a seasoned sales strategist skilled at translating data insights
            into actionable business strategies, considering market conditions and objectives.""",
            verbose=True,
            allow_delegation=True,
            llm=self.llm,
            cache=True
        )

        crm_specialist = Agent(
            role='CRM Specialist',
            goal='Provide CRM insights for: {question}',
            backstory="""You are a CRM expert specializing in customer behavior analysis,
            segmentation, and relationship management strategies.""",
            verbose=True,
            allow_delegation=True,
            llm=self.llm,
            cache=True
        )

        return [data_analyst, sales_strategist, crm_specialist]

    def create_tasks(self, agents: List[Agent]) -> List[Task]:
        data_analyst, sales_strategist, crm_specialist = agents

        # Task 1: Data Analysis
        analysis_task = Task(
            description="""Analyze the sales data from the 'superstore' table to answer: {question}.
            Focus on key metrics (e.g., sales, profit, quantity), trends, and patterns.
            Use SQL queries to extract relevant data and provide a comprehensive analysis. 
            Remember, all tools expect a simple string as input""",
            agent=data_analyst,
            expected_output="""A detailed markdown report containing:
            - Key metrics (sales, profit, etc.)
            - Identified trends and patterns
            - Supporting data points from SQL queries
            - Clear explanations of findings""",
            async_execution=False,
            output_file=f"{self.output_dir}/analysis_report.md"
        )

        # Task 2: Strategy Development
        strategy_task = Task(
            description="""Based on the data analysis for {question}, develop strategic recommendations.
            Consider:
            - Market conditions and competitive landscape
            - Business objectives (growth, profitability, market share)
            - Practical implementation steps""",
            agent=sales_strategist,
            expected_output="""A markdown report containing:
            - Strategic recommendations
            - Actionable implementation plans
            - Expected business impact
            - Alignment with analysis findings""",
            output_file=f"{self.output_dir}/strategy_report.md",
            async_execution=False,
            context=[analysis_task]
        )

        # Task 3: CRM Insights
        crm_task = Task(
            description="""Provide CRM-specific insights for {question} based on sales data.
            Focus on:
            - Customer behavior patterns
            - Segmentation opportunities
            - Relationship management strategies
            Use relevant data points from the analysis.""",
            agent=crm_specialist,
            expected_output="""A markdown report containing:
            - Customer behavior insights
            - Segmentation recommendations
            - CRM strategies for customer retention
            - Supporting data points""",
            output_file=f"{self.output_dir}/crm_report.md",
            async_execution=False,
            context=[analysis_task]
        )

        return [analysis_task, strategy_task, crm_task]

    def create_crew(self):
        agents = self.create_agents()
        tasks = self.create_tasks(agents)

        crew = Crew(
            agents=agents,
            tasks=tasks,
            verbose=True,
            process=Process.sequential,
            cache=True,
            max_rpm=100,
            share_crew=False
        )

        return crew
