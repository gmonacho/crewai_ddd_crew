from pathlib import Path
from tabnanny import verbose

from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from crewai_tools.tools.file_read_tool.file_read_tool import FileReadTool
from crewai_tools.tools.file_writer_tool.file_writer_tool import FileWriterTool

from crewai_poc.tools.python.module.writer import PythonModuleWriter
from crewai_poc.tools.python.package.reader import PythonPackageContextReader


anthropic_llm = LLM(model="anthropic/claude-3-5-sonnet-latest")

_read_the_domain_tool = PythonPackageContextReader(
	name = "Python Domain Package Context Reader",
	description= "Parse and return the domain layer context",
	project_path=Path("/home/gmonacho/projects/saucisses_a_roulettes/ai/crewai_poc/app_poc/src/domain")
)

@CrewBase
class CrewaiPoc:

	@agent
	def domain_expert(self) -> Agent:
		return Agent(
			config=self.agents_config['domain_expert'],
			allow_code_execution=True,
			tools=[
				_read_the_domain_tool
			],
			allow_delegation=True,
			verbose=True,
			llm=anthropic_llm
		)

	@agent
	def domain_developer(self) -> Agent:
		return Agent(
			config=self.agents_config['domain_developer'],
			allow_code_execution=True,
			tools=[
				_read_the_domain_tool,
				PythonModuleWriter(project_path=Path("/home/gmonacho/projects/saucisses_a_roulettes/ai/crewai_poc/app_poc/src/domain"))
			],
			allow_delegation=False,
			verbose=True,
			llm=anthropic_llm
		)

	@task
	def extract_domain_layer_business_logic(self) -> Task:
		return Task(
			config=self.tasks_config['extract_domain_layer_business_logic'],
		)

	@task
	def bring_expertise_on_domain(self) -> Task:
		return Task(
			config=self.tasks_config['bring_expertise_on_domain'],
		)


	@task
	def implement_feature_in_domain(self) -> Task:
		return Task(
			config=self.tasks_config['implement_feature_in_domain'],
		)


	@crew
	def crew(self) -> Crew:
		"""Creates the CrewaiPoc crew"""
		# To learn how to add knowledge sources to your crew, check out the documentation:
		# https://docs.crewai.com/concepts/knowledge#what-is-knowledge

		return Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			process=Process.sequential,
			verbose=True,
			# process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
		)
