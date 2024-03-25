  /**
   * Method to create a placeholder option element for a select element
   * @param {string} placeholderText - The text to be displayed as the placeholder
   * @returns {HTMLOptionElement} - The placeholder option element
   */
  function createSelectPlaceholderElement(placeholderText) {
    var placeholder_option = document.createElement('option');
    placeholder_option.text = placeholderText;
    placeholder_option.selected = true;
    placeholder_option.disabled = true;
    placeholder_option.hidden = true;
  
    return placeholder_option;
  }

  /**
   * Method to fetch the CSRF token from the form on the page
   * @requires A form with a hidden input named "csrfmiddlewaretoken" inserted with {% csrf_token %}
   * @returns {string} - The CSRF token
  */
  function getCsrfToken() {
    return document.getElementsByName("csrfmiddlewaretoken")[0].value;
  }


  /**
   * Gets the current DateTime
   * @param {string} datepickerId - The id of the datepicker input element
   * @returns {Date} - The current date and time
  */
  function setDatePickerMinDateNow(datepickerId)
  {
    // Get current date and time
    var currentDate = new Date();

    // Format date
    var year = currentDate.getFullYear();
    var month = ('0' + (currentDate.getMonth() + 1)).slice(-2); // Month is zero-based
    var day = ('0' + currentDate.getDate()).slice(-2);
    var formattedDate = year + '-' + month + '-' + day;

    // Set min date and time for input element
    var inputElement = document.getElementById(datepickerId);
    inputElement.min = formattedDate;

  }