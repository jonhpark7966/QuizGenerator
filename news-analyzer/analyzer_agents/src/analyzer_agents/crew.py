from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

from analyzer_agents.tools.custom_tool import NaverNewsAPITool, NaverHeadlineTool

from crewai_tools import tool, ScrapeWebsiteTool


import os

import requests

@CrewBase
class AnalyzerAgentsCrew():
	"""AnalyzerAgents crew"""
	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'

	@agent
	def news_headline_crawler(self) -> Agent:
		return Agent(
			config=self.agents_config['news_headline_crawler'],
			tools=[NaverHeadlineTool()],
			verbose=True
		)

	@agent
	def news_crawler(self) -> Agent:
		return Agent(
			config=self.agents_config['news_crawler'],
			tools=[NaverNewsAPITool(), ScrapeWebsiteTool()],
			verbose=True
		)

	@agent
	def news_curator(self) -> Agent:
		return Agent(
			config=self.agents_config['news_curator'],
			verbose=True
		)

	@agent
	def news_analyzer(self) -> Task:
		return Agent(
			config=self.agents_config['news_analyzer'],
		)

	@agent
	def translator(self) -> Task:
		return Agent(
			config=self.agents_config['translator'],
		)

	@agent
	def quiz_generator(self) -> Task:
		return Agent(
			config=self.agents_config['quiz_generator'],
		)

	@task
	def headline_extraction_task(self) -> Task:
		return Task(
			config=self.tasks_config['headline_extraction_task'],
			output_file='headlines.json'
		)

	@task
	def crawling_task(self) -> Task:
		return Task(
		    input_files=['headlines.json'],
			config=self.tasks_config['crawling_task'],
			output_file='news.json'
		)

	@task
	def curation_task(self) -> Task:
		return Task(
		    input_files=['news.json'],
			config=self.tasks_config['curation_task'],
			output_file='curated_news.json'
		)

	@task
	def analysis_task(self) -> Task:
		return Task(
		    input_files=['curated_news.json'],
			config=self.tasks_config['analysis_task'],
			output_file='analyzed_news.json'
		)

	@task
	def translation_task(self) -> Task:
		return Task(
		    input_files=['analyzed_news.json'],
			config=self.tasks_config['translation_task'],
			output_file='korean_analyzed_news.json'
		)

	@task
	def quiz_creation_task(self) -> Task:
		return Task(
		    input_files=['korean_analyzed_news.json'],
			config=self.tasks_config['quiz_creation_task'],
			output_file='quiz.json'
		)

	@crew
	def crew(self) -> Crew:
		"""Creates the AnalyzerAgents crew"""
		return Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			process=Process.sequential,
			verbose=True,
			# process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
		)
