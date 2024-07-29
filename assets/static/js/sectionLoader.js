function loadSection(sectionName){
    $('.section').each((i, el) => {
        if (el.id == sectionName){
            // console.log('Section: ' + el.id)
            // Show section
            if (el.classList.contains('sectionHide')){
                el.classList.replace('sectionHide', 'sectionShow');
            }
            // Outline current section in navbar
            // Outline Title
            if (document.getElementById(sectionName + 'Title').classList.contains('headingHover')){
                document.getElementById(sectionName + 'Title').classList.replace('headingHover', 'headingDisableHover');
            }
            // Outline Logo
            if (document.getElementById(sectionName + 'Logo').classList.contains('headingHover')){
                document.getElementById(sectionName + 'Logo').classList.replace('headingHover', 'headingDisableHover');
            }
        }
        else {
            // console.log('Not Section: ' + el.id)
            // Remove nonactive sections
            if (el.classList.contains('sectionShow')){
                el.classList.replace('sectionShow', 'sectionHide');
            }
            if (document.getElementById(el.id + 'Title') != null){
                // Remove nonactive section titles
                if (document.getElementById(el.id + 'Title').classList.contains('headingDisableHover')){
                    document.getElementById(el.id + 'Title').classList.replace('headingDisableHover', 'headingHover');
                }
                // Remove nonactive section logos
                if (document.getElementById(el.id + 'Logo').classList.contains('headingDisableHover')){
                    document.getElementById(el.id + 'Logo').classList.replace('headingDisableHover', 'headingHover');
                }
            }
        }
    });
}