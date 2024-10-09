
$(".number-tab-steps").steps({
  headerTag: "h6",
  bodyTag: "fieldset",
  transitionEffect: "fade",
  titleTemplate: '#index# #title#',
  labels: {
      finish: 'Submit'
  },
  onFinished: function (event, currentIndex) {
      alert("Form submitted.");
  }
});