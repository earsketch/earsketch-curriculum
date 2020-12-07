var ideScope;
var layoutScope;
var gmLanguage = {
    'lang' : ''
};
var gmToggle = {
    'toggleCurr' : true
}
var gmWindow; 

angular.element('[ng-controller="ideController"]').ready(function () {
    scope =  $('[ng-controller="ideController"]').scope()
     
    gmLanguage['lang'] = scope.curriculumLanguage;
    
    // listen for language changes
    scope.$on('language', function (event, val) {
        gmLanguage['lang'] = val;
        gmWindow  = document.getElementById("frame").contentWindow;
        gmWindow.postMessage(gmLanguage, "*");
    });
});

angular.element('[ng-controller="layoutController"]').ready(function () {
    layoutScope = $('[ng-controller="layoutController"]').scope()

    // listen for toggleCurriculum changes
    layoutScope.$on('toggleCurr', function (event, val) {
        gmToggle['toggleCurr'] = val;
        gmWindow  = document.getElementById("frame").contentWindow;
        gmWindow.postMessage(gmToggle, "*");
    });
});

//copy code into ES Script
window.addEventListener('message', function(message) {
    if (message.isTrusted) {
       
        // check if message.data is a String
        if(typeof message.data === 'string' && message.data != "langrequest") 
            angular.element($('#devctrl')).scope().pasteCurriculumCode(message.data);

        else if (message.data == "langrequest") {
            gmWindow  = document.getElementById("frame").contentWindow;
            gmWindow.postMessage(gmLanguage, "*");
        }
    }
});