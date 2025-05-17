// This script adds target="_blank" and rel="noopener noreferrer" to external links in the sidebar.
// These links are defined in the mkdocs.yml file under the nav section.

document.addEventListener("DOMContentLoaded", function () {
    const currentHost = window.location.host;
    const sidebarLinks = document.querySelectorAll(".md-nav a, .nav a"); // adjust for your theme
  
    sidebarLinks.forEach(function (link) {
      try {
        const url = new URL(link.href);
        if (url.host !== currentHost) {
          link.setAttribute("target", "_blank");
          link.setAttribute("rel", "noopener noreferrer");
        }
      } catch (e) {
        // Ignore invalid URLs (like internal hash links)
      }
    });
  });
  