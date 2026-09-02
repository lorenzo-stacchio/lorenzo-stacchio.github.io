---
# Leave the homepage title empty to use the site title
title: ''
date: 2022-10-24
type: landing

sections:
  - block: about.biography
    id: about
    content:
      title: Biography
      # Choose a user profile to display (a folder name within `content/authors/`)
      username: admin

  - block: experience
    id: experience
    content:
      title: Experience
      date_format: Jan 2006
      items:
        - title: Research Fellow in Computer Science
          company: University of Macerata, Department of Political Sciences, Communication and International Relations (SPOCRI)
          company_url: 'https://www.unimc.it/en?set_language=en'
          location: Macerata, Italy
          date_start: '2024-02-01'
          date_end: ''
          description: |2-
              Research, teaching and technology transfer within the VRAI laboratory, on consumer behaviour analysis in retail through top-view RGB-D cameras, and more broadly on eXtended Reality and Artificial Intelligence. Supervised by Prof. Emanuele Frontoni.

        - title: Adjunct Lecturer
          company: Università Politecnica delle Marche, Department of Information Engineering
          company_url: 'https://www.univpm.it/'
          location: Ancona, Italy
          date_start: '2025-09-01'
          date_end: ''
          description: Advanced programming for video games and virtual reality systems (9 ECTS), B.Sc. in Information Engineering for Video Games and Virtual Reality.

        - title: Lecturer, Ph.D. Programme
          company: University of Milano-Bicocca, Economics, Statistics and Data Science (ECOSTATDATA)
          company_url: 'https://www.unimib.it/'
          location: Milan, Italy
          date_start: '2024-10-01'
          date_end: ''
          description: Deep Learning and Computer Vision for Business (2 ECTS), taught annually within the doctoral programme.

        - title: Adjunct Lecturer
          company: University of Macerata
          company_url: 'https://www.unimc.it/en?set_language=en'
          location: Macerata, Italy
          date_start: '2024-06-01'
          date_end: ''
          description: Graphics and Virtual Reality (4 ECTS), within the 60-ECTS teacher qualification pathway.

        - title: Visiting Researcher
          company: Graz University of Technology
          company_url: 'https://www.tugraz.at/en/home'
          location: Graz, Austria
          date_start: '2023-02-01'
          date_end: '2023-05-31'
          description: Research on diffusion models for temporally coherent rendering generation, hosted by Prof. Denis Kalkofen.
    design:
      columns: '2'

  - block: collection
    id: selected
    content:
      title: Selected Publications
      text: Here are reported recent works that best represents his research.
      filters:
        folders:
          - publication
        featured_only: true
    design:
      columns: '2'
      view: citation

  - block: collection
    id: recentpub
    content:
      title: Recent Publications
      count: 6
      text: |-
        {{% callout note %}}
        Browse the complete record of 44 publications, filterable by type and topic, on the [publications page](./publication/).
        {{% /callout %}}
      filters:
        folders:
          - publication
        exclude_featured: false
    design:
      columns: '2'
      view: citation

  - block: collection
    id: conferences
    content:
      title: Workshops & Chairing
      text: Workshops and sessions organised or chaired at international venues.
      filters:
        folders:
          - conferences
    design:
      columns: '2'
      view: compact

  - block: collection
    id: talks
    content:
      title: Invited Talks & Lectures
      filters:
        folders:
          - event
    design:
      columns: '2'
      view: compact

  - block: accomplishments
    id: awards
    content:
      title: Awards & Roles
      date_format: Jan 2006
      items:
        - title: National Scientific Qualification (ASN), Associate Professor
          organization: Italian Ministry of University and Research
          organization_url: ''
          date_start: '2026-07-30'
          date_end: ''
          description: Qualification for the role of Associate Professor in Information Processing Systems (IINF-05/A), valid until July 2038.
          url: ''

        - title: Editor of Distinction Award, Author Service
          organization: Springer Nature
          organization_url: 'https://www.springernature.com/'
          date_start: '2026-01-01'
          date_end: ''
          description: Awarded to editors in the top 20% for time to first decision.
          url: ''

        - title: Best Paper Award, IEEE VR 2025
          organization: 32nd IEEE Conference on Virtual Reality and 3D User Interfaces
          organization_url: ''
          date_start: '2025-03-01'
          date_end: ''
          description: 'For "MineVRA: Exploring the Role of Generative AI-Driven Content Development in XR Environments through a Context-Aware Approach".'
          url: ''

        - title: Associate Editor, The Visual Computer
          organization: Springer
          organization_url: 'https://link.springer.com/journal/371/editorial-board'
          date_start: '2025-02-17'
          date_end: ''
          description: Also Lead Guest Editor of the Virtual Reality special issue on Agentic AI for Extended Reality.
          url: 'https://link.springer.com/journal/371/editorial-board'

        - title: Best Project, XR&AI Summer School
          organization: XR and AI for enhancing cultural and territorial heritage, Matera
          organization_url: ''
          date_start: '2022-09-10'
          date_end: ''
          description: Winning pitch for a generative AI and augmented reality solution supporting cultural heritage.
          url: ''

        - title: Best Poster, VisMac 2020 Doctoral School
          organization: VisMac
          organization_url: ''
          date_start: '2021-10-06'
          date_end: ''
          description: 'For "IMAGO: a family photo album dataset for a socio-historical analysis of the twentieth century".'
          url: ''
    design:
      columns: '2'

  - block: markdown
    id: projects
    content:
      title: Research Projects
      text: |-
        **Work package lead**

        - **[STEM Skills for Humanities](https://stem4humanities.eu/)** — Erasmus+ (2023-1-IT02-KA220-HED-000164647). Lead of Work Package 2, "Upskilling of Humanities Professors": designing and delivering training that builds STEM competence among humanities faculty. *Sept 2024 – Oct 2025.*
        - **[AGRITECH.EU — Digital Agriculture for Sustainable Development](https://www.agridigital-skills.eu/)** — DIGITAL-2022-SKILLS-03 (Project N° 101123258). Lead of Work Packages 2 and 3, covering the shared training catalogue architecture and immersive AI- and XR-based modules for digital agriculture, and their integration into higher education curricula. *May 2025 – present.*

        **Participation**

        - **WHIM — Understanding WHat Is Mine** — PRIN 2022 (2022LYRT8E_002), on the sense of ownership over objects.
        - **CAPPELLAI** — AI supporting demand analysis and creativity in the hat-making sector. PR FESR Marche 2021–2027.
        - **PASTA** — Advanced and sustainable productivity for artisanal transformation 4.0. PR FESR Marche 2021–2027.
        - **MuseAI** — Enhancing museum interactions with AI. PR FESR Marche 2021–2027.
        - **IDEA** — Industrial defect identification in footwear production via deep learning object detection.
        - **G-NEXT** — Sustainable and digital product innovation. PR FESR Marche 2021–2027.
    design:
      columns: '1'
---
