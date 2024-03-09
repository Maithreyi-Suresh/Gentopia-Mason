from typing import AnyStr, Optional
from googlesearch import search
from gentopia.tools.basetool import *
import PyPDF2
import requests

class GoogleSearchArgs(BaseModel):
    query: str = Field(..., description="a search query")
    pdf_link: Optional[str] = Field(None, description="link to a PDF file")

class GoogleSearch(BaseTool):
    """Tool that adds the capability to query the Google search API and read PDF files."""

    name = "google_search"
    description = ("A search engine retrieving top search results as snippets from Google."
                   "Input should be a search query.")

    args_schema: Optional[Type[BaseModel]] = GoogleSearchArgs

    def _run(self, query: AnyStr, pdf_link: Optional[str] = None) -> str:
        results = search(query, advanced=True)
        output = '\n\n'.join([str(item) for item in results])
        if pdf_link:
            pdf_text = self._read_pdf(pdf_link)
            output += "\n\nPDF Text:\n" + pdf_text
        return output

    async def _arun(self, *args: Any, **kwargs: Any) -> Any:
        raise NotImplementedError

    def _read_pdf(self, pdf_link: str) -> str:
        response = requests.get(pdf_link)
        with open("temp_pdf.pdf", "wb") as f:
            f.write(response.content)
        text = ""
        with open("temp_pdf.pdf", "rb") as file:
            reader = PyPDF2.PdfFileReader(file)
            for page in range(reader.numPages):
                text += reader.getPage(page).extractText()
        return text

if __name__ == "__main__":
    # Example usage of GoogleSearch tool
    ans = GoogleSearch()._run("Attention for transformer")
    print(ans)
