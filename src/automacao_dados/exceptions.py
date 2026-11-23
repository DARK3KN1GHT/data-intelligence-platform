class AutomationError(Exception):
    """Erro base da plataforma."""


class IngestionError(AutomationError):
    """Falha durante a importação de dados."""


class DataValidationError(AutomationError):
    """Dados incompatíveis com as regras de validação."""


class ProcessingError(AutomationError):
    """Falha durante o processamento."""


class ReportGenerationError(AutomationError):
    """Falha durante a geração de relatórios."""
