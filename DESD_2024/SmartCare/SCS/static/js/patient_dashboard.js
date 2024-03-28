
/**
 * Method to populate the practitioners select element with available practitioners
 * @param {Array} practitioners - The practitioners to be populated
 */
function populatePractitioners(practitioners) {
  var practitionerSelect = document.getElementById('practitioner');
  practitionerSelect.innerHTML = "";
  
  // creating placeholder for selecting a practitioner
  placeholder_option = createSelectPlaceholderElement("Select a Practitioner")
  practitionerSelect.appendChild(placeholder_option);

  practitioners.doctors.forEach(doctor => {
    var option = document.createElement('option');
    option.value = doctor[1];
    option.text = doctor[0];
    practitionerSelect.appendChild(option);
  });

  practitioners.nurses.forEach(nurse => {
    var option = document.createElement('option');
    option.value = nurse[1];
    option.text = nurse[0];
    practitionerSelect.appendChild(option);
  });
}

/**
 * Method to populate the time slots select element with available time slots
 * @param {Array} timeSlots - The time slots to be populated
 */
function populateTimeSlots(timeSlots) {
  var timeSlotSelect = document.getElementById('timeSlot');
  timeSlotSelect.innerHTML = "";

  // creating placeholder for selecting a practitioner
  placeholder_option = createSelectPlaceholderElement("Select a Time Slot")
  timeSlotSelect.appendChild(placeholder_option);
  
  timeSlots.forEach(timeSlot => {
    var option = document.createElement('option');
    option.value = timeSlot;
    option.text = timeSlot;
    timeSlotSelect.appendChild(option);
  });

}

/**
 * Method to get practitioners by day and service when service and date selected
 * @param {HTMLSelectElement} service - The select element for the service
 * @param {HTMLInputElement} bookingDate - The input element for the booking date
 */
function getPractitionersByDayAndService(service, bookingDate) {
  // Create a FormData object and append the date value
  var formData = new FormData();
  formData.append("bookingDate", bookingDate.value);
  formData.append("service", service.value);
  var token = getCsrfToken();
  fetch('retrieve_practitioners_by_day_and_service', {
    method: 'POST',
    headers: {
            'X-CSRFToken': token
            },
    body: formData
  })
  .then(response => response.json())
  .then(data => {
    if (data.success) {
      populatePractitioners(data.practitioners);
      document.getElementById('practitioner').disabled = false;
    } else {
      
      alert(data.error);
    }
  });
}

/**
 * Method to get time slots by day and practitioner when date and practitioner selected
 * @param {HTMLInputElement} bookingDate - The input element for the booking date
 * @param {HTMLSelectElement} practitioner - The select element for the practitioner
 */
function getTimeSlotsByDayAndPractitioner(bookingDate, practitioner) {
  // Create a FormData object and append the date value
  var formData = new FormData();
  formData.append("bookingDate", bookingDate.value);
  formData.append("practitioner", practitioner.value);
  var token = getCsrfToken();
  fetch('retrieve_time_slots_by_day_and_practitioner', {
    method: 'POST',
    headers: {
            'X-CSRFToken': token
            },
    body: formData
  })
  .then(response => response.json())
  .then(data => {
    if (data.success) {
      populateTimeSlots(data.timeSlots);
      document.getElementById('timeSlot').disabled = false;
    } else {
      
      alert(data.error);
    }
  });
}


/**
 * Method to make a patient appointment booking
 * @param {HTMLFormElement} form - The form element to be submitted
 */
function makePatientAppointmentBooking(form) {
  var formData = new FormData(form);
  var token = getCsrfToken() ;

  if (formData.get('bookingDate') === "") {
    alert("Please select a date");
    return;
  }

  else if (formData.get('practitioner') === "") {
    alert("Please select a practitioner");
    return;
  }

  else if (formData.get('service') === "") {
    alert("Please select a service");
    return;
  }

  else if (formData.get('timeSlot') === "") {
    alert("Please select a time slot");
    return;
  }

  fetch('patient_appointment_booking', {
  method: 'POST',
  headers: {
          'X-CSRFToken': token
          },

body: formData
})
.then(response => response.json())
.then(data => {
if (data.success) {
  // show success message
  // refresh page
  alert('Appointment booked successfully');

  // resetting form fields
  service = document.getElementById('service')
  service.value = createSelectPlaceholderElement("Select a Service");

  bookingDate = document.getElementById('bookingDate')
  bookingDate.value = createSelectPlaceholderElement("Select a Date");
  bookingDate.disabled = true;

  practitionerSelect = document.getElementById('practitioner')
  practitionerSelect.value = createSelectPlaceholderElement("Select a Practitioner");
  practitionerSelect.disabled = true;

  timeSlotSelect = document.getElementById('timeSlot')
  timeSlotSelect.value = createSelectPlaceholderElement("Select a Time Slot");
  timeSlotSelect.disabled = true;

  reason = document.getElementById('reason').value = "";    

} else {
  
  alert(data.error);
}
});

}