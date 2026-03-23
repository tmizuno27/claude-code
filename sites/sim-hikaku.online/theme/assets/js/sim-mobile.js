/* ============================================
   SIM比較オンライン — Mobile UX Enhancements
   - Back to Top button
   - Table scroll indicators
   ============================================ */
(function () {
  "use strict";

  /* --- Back to Top Button --- */
  var btn = document.createElement("div");
  btn.className = "back-to-top";
  btn.setAttribute("aria-label", "ページ上部に戻る");
  btn.setAttribute("role", "button");
  document.body.appendChild(btn);

  var scrollTimer;
  window.addEventListener("scroll", function () {
    if (scrollTimer) return;
    scrollTimer = requestAnimationFrame(function () {
      if (window.scrollY > 300) {
        btn.classList.add("visible");
      } else {
        btn.classList.remove("visible");
      }
      scrollTimer = null;
    });
  });

  btn.addEventListener("click", function () {
    window.scrollTo({ top: 0, behavior: "smooth" });
  });

  /* --- Table Scroll Indicators --- */
  function wrapTables() {
    var tables = document.querySelectorAll(".entry-content table");
    tables.forEach(function (table) {
      if (table.parentElement.classList.contains("table-inner")) return;
      var wrapper = document.createElement("div");
      wrapper.className = "table-scroll-wrapper";
      var inner = document.createElement("div");
      inner.className = "table-inner";
      table.parentNode.insertBefore(wrapper, table);
      inner.appendChild(table);
      wrapper.appendChild(inner);

      function checkScroll() {
        var scrollable = inner.scrollWidth > inner.clientWidth + 2;
        wrapper.classList.toggle("has-scroll", scrollable);
        var atEnd = inner.scrollLeft + inner.clientWidth >= inner.scrollWidth - 2;
        wrapper.classList.toggle("scrolled-end", atEnd);
      }

      inner.addEventListener("scroll", checkScroll);
      window.addEventListener("resize", checkScroll);
      checkScroll();
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", wrapTables);
  } else {
    wrapTables();
  }
})();
