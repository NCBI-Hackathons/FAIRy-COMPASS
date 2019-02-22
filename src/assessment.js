import process from 'process'
import readline from 'readline'

const any = A => {
  for (const a of A) {
    if (a)
      return true
  }
  return false
}

const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout,
  terminal: false,
})

rl.on('line', line => {
  const data = JSON.parse(line)
  const assessment = {
    target: {
      title: data.github.full_name,
      description: data.github.description || '',
      tags: Array.isArray(data.extruct.microdata[0].properties.keywords) ? data.extruct.microdata[0].properties.keywords.join(', ') : '',
      url: data.github.html_url,
      projects: [71],
      rubrics: [29],
    },
    assessment: {
      project: 71,
      rubric: 29,
      answers: [
        // Automatable
        { // The tool has a Dockerfile/Singularity recipe?
          metric: 129,
          answer: any(data.ls.map(file => file.name === "Dockerfile" || file.name === "docker-compose.yml")) && 1.0 || 0.0,
          comment: `Dockerfile or docker-compose.yml in ${data.ls.map(file => file.name).join(', ')}`,
        },
        { // ReadMe (existence of with more than one line)
          metric: 130,
          answer: any(data.ls.map(file => file.name === "README" || file.name === "README.md")) && 1.0 || 0.0,
          comment: `README or README.md in ${data.ls.map(file => file.name).join(', ')}`,
        },
        { // Licensing information is provided on the tool’s homepage.
          metric: 9,
          answer: data.github.license !== undefined ? 1.0 : 0.0,
          comment: (data.github.license || {}).name || null,
        },
        { // Source code is shared in a public repository and is documented.
          metric: 5,
          answer: 1.0,
        },
        {  // The tool has a unique title.
          metric: 60,
          answer: data.github.full_name.length > 0 ? 1.0 : 0.0,
          comment: data.github.full_name,
        },
        { // The tool has an informative description.
          metric: 131,
          answer: (data.github.description || '').length > 0 ? 1.0 : 0.0,
          comment: data.github.description || '',
        },
        { // The tool can be freely downloaded or accessed from a webpage.
          metric: 2,
          answer: data.github.html_url.length > 0 ? 1.0 : 0.0,
          comment: data.github.html_url,
        },
        // NICE TO HAVE
        { // Contact information is provided for the creator(s) of the tool.
          metric: 27,
          query: null,
        },
        { // Information describing how to cite the tool is provided
          metric: 28,
          answer: null,
        },
        { // Domain?
          metric: 102,
          answer: null,
        },
        { // Versioning
          metric: 6,
          answer: null,
        },
        { // Languages/File types
          metric: 95,
          answer: null,
        },
        { // APIs
          metric: 8,
          answer: null,
        },
        { // File provenance (including authorship history)
          metric: 118,
          answer: null,
        }
      ]
    }
  }
  console.log(JSON.stringify(assessment))
})
