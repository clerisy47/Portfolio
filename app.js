(function () {
    const escapeHtml = (value) =>
        String(value ?? "")
            .replace(/&/g, "&amp;")
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;")
            .replace(/"/g, "&quot;")
            .replace(/'/g, "&#39;");

    const mdToHtml = (text) => {
        let out = escapeHtml(text);
        out = out.replace(/\*\*(.+?)\*\*/g, "<strong>$1</strong>");
        out = out.replace(/\*(.+?)\*/g, "<em>$1</em>");
        return out;
    };

    const plainText = (text) =>
        String(text ?? "")
            .replace(/\*\*(.+?)\*\*/g, "$1")
            .replace(/\*(.+?)\*/g, "$1");

    const bulletText = (bullet) =>
        typeof bullet === "string" ? bullet : bullet?.text ?? "";

    const contactByType = (data, type) =>
        (data.contact || []).find((item) => item.type === type);

    const formatDates = (dates) =>
        String(dates ?? "")
            .replace(/\//g, " ")
            .replace(/–/g, "-")
            .replace(/\b0?(\d{1,2})\b(?=\s+\d{4})/g, (_, m) => {
                const months = [
                    "",
                    "Jan",
                    "Feb",
                    "Mar",
                    "Apr",
                    "May",
                    "Jun",
                    "Jul",
                    "Aug",
                    "Sep",
                    "Oct",
                    "Nov",
                    "Dec",
                ];
                const n = Number(m);
                return n >= 1 && n <= 12 ? months[n] : m;
            });

    const renderStats = (stats) =>
        (stats || [])
            .map((stat) => {
                const lines = escapeHtml(stat.label).split(/\s+/);
                const labelHtml =
                    lines.length > 1
                        ? `${lines.slice(0, -1).join(" ")} <br /> ${lines.at(-1)}`
                        : lines[0] || "";
                return `
                <div class="about-item">
                    <div class="abt-text">
                        <p class="large-text">${escapeHtml(stat.value)}</p>
                        <p class="small-text">${labelHtml}</p>
                    </div>
                </div>`;
            })
            .join("");

    const renderSkills = (skills) =>
        (skills || [])
            .map(
                (group) => `
            <div class="skills-category">
                <h5 class="category-title">${escapeHtml(group.category)}</h5>
                <div class="skills-cards">
                    ${(group.items || [])
                        .map((item) => {
                            const name = item.displayName || item.name;
                            const icon = item.icon
                                ? `<img src="${escapeHtml(item.icon)}" alt="${escapeHtml(name)}">`
                                : "";
                            return `
                            <div class="skill-card">
                                ${icon}
                                <p>${escapeHtml(name)}</p>
                            </div>`;
                        })
                        .join("")}
                </div>
            </div>`
            )
            .join("");

    const renderExperience = (experience) =>
        (experience || [])
            .map((job) => {
                const bullets = (job.bullets || [])
                    .map((b) => `• ${mdToHtml(bulletText(b))}`)
                    .join("<br><br>");
                return `
                <div class="timeline-item">
                    <div class="tl-icon">
                        <i class="fas fa-briefcase"></i>
                    </div>
                    <p class="tl-duration">${escapeHtml(formatDates(job.dates))}</p>
                    <h5>${escapeHtml(job.title)}<span> <br> ${escapeHtml(job.company)}</span></h5>
                    <p>
                        ${mdToHtml(job.description || "")}
                        ${bullets ? `<br><br>${bullets}` : ""}
                    </p>
                </div>`;
            })
            .join("");

    const renderEducation = (education) =>
        (education || [])
            .map(
                (edu) => `
            <div class="timeline-item">
                <div class="tl-icon">
                    <i class="fas fa-briefcase"></i>
                </div>
                <p class="tl-duration">${escapeHtml(edu.dates)}</p>
                <h5>${escapeHtml(edu.degree)}<span> <br> ${escapeHtml(edu.school)}</span></h5>
                <p>
                    ${escapeHtml(edu.location)} <br><br>
                    ${escapeHtml(edu.detail)}
                </p>
            </div>`
            )
            .join("");

    const renderPortfolio = (portfolio) =>
        (portfolio || [])
            .map(
                (project) => `
            <div class="portfolio-item">
                <div class="image">
                    <img src="${escapeHtml(project.image)}" alt="${escapeHtml(project.title)}">
                </div>
                <div class="hover-items">
                    <h3>${escapeHtml(project.title)}</h3>
                    <p>${escapeHtml(project.description)}</p>
                    <div class="icons">
                        <a href="${escapeHtml(project.url)}" class="icon" target="_blank" rel="noopener">
                            <i class="fab fa-github"></i>
                        </a>
                    </div>
                </div>
            </div>`
            )
            .join("");

    const renderSocial = (social) =>
        (social || [])
            .map(
                (item) => `
            <a href="${escapeHtml(item.url)}" target="_blank" rel="noopener">
                <i class="${escapeHtml(item.icon)}"></i>
            </a>`
            )
            .join("");

    const renderContactInfo = (data) => {
        const email = contactByType(data, "email");
        const phone = contactByType(data, "phone");
        const phoneLabel = (phone?.label || "").replace(/^\+977/, "");
        const rows = [
            {
                icon: "fas fa-map-marker-alt",
                label: "Location",
                value: data.location,
            },
            {
                icon: "fas fa-envelope",
                label: "Email",
                value: email?.label,
            },
            {
                icon: "fas fa-user-graduate",
                label: "Education",
                value: data.educationShort,
            },
            {
                icon: "fas fa-user-graduate",
                label: "Mobile Number",
                value: phoneLabel,
            },
            {
                icon: "fas fa-globe-africa",
                label: "Languages",
                value: data.spokenLanguages,
            },
        ];

        return rows
            .filter((row) => row.value)
            .map(
                (row) => `
            <div class="contact-item">
                <div class="icon">
                    <i class="${row.icon}"></i>
                    <span>${escapeHtml(row.label)}</span>
                </div>
                <p>
                    <span>${escapeHtml(row.value)}</span>
                </p>
            </div>`
            )
            .join("");
    };

    const listRenderers = {
        stats: (data) => renderStats(data.stats),
        skills: (data) => renderSkills(data.skills),
        experience: (data) => renderExperience(data.experience),
        education: (data) => renderEducation(data.education),
        portfolio: (data) => renderPortfolio(data.portfolio),
        social: (data) => renderSocial(data.social),
        contactInfo: (data) => renderContactInfo(data),
    };

    const applyBindings = (data) => {
        document.title = `${data.name} - Portfolio`;

        document.querySelectorAll("[data-bind]").forEach((el) => {
            const key = el.getAttribute("data-bind");
            if (key in data) el.textContent = plainText(data[key]);
        });

        document.querySelectorAll("[data-bind-html]").forEach((el) => {
            const key = el.getAttribute("data-bind-html");
            if (key in data) el.innerHTML = mdToHtml(data[key]);
        });

        document.querySelectorAll("[data-bind-href]").forEach((el) => {
            const key = el.getAttribute("data-bind-href");
            if (key in data && data[key]) el.setAttribute("href", data[key]);
        });

        document.querySelectorAll("[data-bind-src]").forEach((el) => {
            const key = el.getAttribute("data-bind-src");
            if (key in data && data[key]) el.setAttribute("src", data[key]);
        });

        document.querySelectorAll("[data-bind-alt]").forEach((el) => {
            const key = el.getAttribute("data-bind-alt");
            if (key in data && data[key]) el.setAttribute("alt", plainText(data[key]));
        });

        document.querySelectorAll("[data-bind-list]").forEach((el) => {
            const key = el.getAttribute("data-bind-list");
            const renderer = listRenderers[key];
            if (renderer) el.innerHTML = renderer(data);
        });
    };

    const initNavAndTheme = () => {
        const navLinks = document.querySelectorAll(".nav-link");
        const themeBtn = document.querySelector(".theme-btn");

        window.addEventListener("scroll", () => {
            let current = "";
            const sections = document.querySelectorAll("section, header");

            sections.forEach((section) => {
                const sectionTop = section.offsetTop;
                if (pageYOffset >= sectionTop - 200) {
                    current = section.getAttribute("id");
                }
            });

            navLinks.forEach((link) => {
                link.classList.remove("active-nav");
                if (link.getAttribute("href").slice(1) === current) {
                    link.classList.add("active-nav");
                }
            });
        });

        navLinks.forEach((link) => {
            link.addEventListener("click", (e) => {
                e.preventDefault();
                const targetSection = document.querySelector(link.getAttribute("href"));
                if (targetSection) {
                    targetSection.scrollIntoView({ behavior: "smooth" });
                }
            });
        });

        themeBtn.addEventListener("click", () => {
            document.body.classList.toggle("light-mode");
            localStorage.setItem(
                "theme",
                document.body.classList.contains("light-mode") ? "light" : "dark"
            );
        });

        if (localStorage.getItem("theme") === "light") {
            document.body.classList.add("light-mode");
        }
    };

    const boot = async () => {
        initNavAndTheme();
        try {
            const response = await fetch("data.json", { cache: "no-store" });
            if (!response.ok) throw new Error(`Failed to load data.json (${response.status})`);
            const data = await response.json();
            applyBindings(data);
        } catch (error) {
            console.error(error);
        }
    };

    boot();
})();
