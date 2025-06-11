from crewai import Agent, Task, Crew, Process
from typing import List
from modules.utils import *

class SalesAnalystAgent:
    def __init__(self):
        self.data = load_data()
        self.llm = load_llm()
        
    def create_agents(self) -> List[Agent]:
        # Data Analyst Agent
        data_analyst = Agent(
            role='Data Analyst',
            goal='Analyze sales data and provide insights',
            backstory="""You are an expert data analyst with years of experience in sales analysis.
            You excel at finding patterns and trends in sales data.""",
            verbose=True,
            allow_delegation=True,
            llm=self.llm
        )
        
        # Sales Strategist Agent
        sales_strategist = Agent(
            role='Sales Strategist',
            goal='Provide strategic recommendations based on sales analysis',
            backstory="""You are a seasoned sales strategist who can turn data insights into
            actionable business recommendations.""",
            verbose=True,
            allow_delegation=True,
            llm=self.llm
        )
        
        # CRM Specialist Agent
        crm_specialist = Agent(
            role='CRM Specialist',
            goal='Analyze customer behavior and provide CRM insights',
            backstory="""You are a CRM expert who understands customer behavior patterns
            and can provide valuable insights for customer relationship management.""",
            verbose=True,
            allow_delegation=True,
            llm=self.llm
        )
        
        return [data_analyst, sales_strategist, crm_specialist]
    
    def create_tasks(self, agents: List[Agent]) -> List[Task]:
        data_analyst, sales_strategist, crm_specialist = agents
        
        # Task 1: Data Analysis
        analysis_task = Task(
            description="""Analyze the sales data and provide insights related to: {question}
            Focus on key metrics, trends, and patterns in the data.""",
            agent=data_analyst,
            expected_output="A detailed analysis of sales data with key metrics, trends, and patterns. Formatted as markdown",
            output_file="output/analysis_report.md"
        )
        
        # Task 2: Strategy Development
        strategy_task = Task(
            description="""Based on the data analysis, develop strategic recommendations for: {question}
            Consider market conditions, competition, and business objectives.""",
            agent=sales_strategist,
            expected_output="Strategic recommendations and action plans based on the data analysis. Formatted as markdown",
            output_file="output/strategy_report.md"
        )
        
        # Task 3: CRM Insights
        crm_task = Task(
            description="""Provide CRM-specific insights and recommendations for: {question}
            Focus on customer behavior, segmentation, and relationship management strategies.""",
            agent=crm_specialist,
            expected_output="CRM insights and customer-focused recommendations. Formatted as markdown",
            output_file="output/crm_report.md"
        )
        
        return [analysis_task, strategy_task, crm_task]
    
    def create_crew(self):
        agents = self.create_agents()
        tasks = self.create_tasks(agents)
        
        crew = Crew(
            agents=agents,
            tasks=tasks,
            verbose=True,
            process=Process.sequential
        )
        
        return crew