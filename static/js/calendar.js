let selectedDate = null;
let selectedTime = null;
let month = new Date().getMonth();
let year = new Date().getFullYear();

const isPastDate = (date) => {
    const today = new Date();
    today.setHours(0, 0, 0, 0);
    return date < today;
};

const updateCalendar = () => {
    const calendarElement = document.getElementById('calendar');
    const monthNames = [
        "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", 
        "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
    ];

    const firstDayOfMonth = new Date(year, month, 1);
    const lastDayOfMonth = new Date(year, month + 1, 0);
    const totalDays = lastDayOfMonth.getDate();
    const firstDayOfWeek = firstDayOfMonth.getDay();

    let calendarHTML = `<h2>${monthNames[month]} ${year}</h2>`;
    calendarHTML += '<div class="calendar-grid">';
    const weekdays = ['Dom', 'Lun', 'Mar', 'Mié', 'Jue', 'Vie', 'Sáb'];
    weekdays.forEach(day => {
        calendarHTML += `<div class="calendar-header">${day}</div>`;
    });

    let dayCount = 1;
    for (let row = 0; row < 6; row++) {
        for (let col = 0; col < 7; col++) {
            if (row === 0 && col < firstDayOfWeek) {
                calendarHTML += '<div class="calendar-day"></div>';
            } else if (dayCount <= totalDays) {
                const dayDate = `${year}-${month + 1}-${dayCount}`;
                calendarHTML += `
                    <div class="calendar-day" data-date="${dayDate}">
                        <span>${dayCount}</span>
                        <div class="status"></div>
                    </div>`;
                dayCount++;
            }
        }
    }
    calendarHTML += '</div>';
    calendarElement.innerHTML = calendarHTML;

    const calendarDays = document.querySelectorAll('.calendar-day');
    calendarDays.forEach(day => {
        const dayDate = new Date(day.getAttribute('data-date'));
        if (isPastDate(dayDate)) {
            day.classList.add('disabled');
            day.style.backgroundColor = '#ccc';
            day.style.pointerEvents = 'none';
        }
        day.addEventListener('click', function () {
            selectedDate = this.getAttribute('data-date');
            showAvailableHours(selectedDate);
            showApprovedReservations(selectedDate);
        });
    });
};

const getApprovedReservations = (selectedDate) => {
    return fetch(`/get_reservations/${selectedDate}`)
        .then(response => response.json())
        .then(data => data);
};

const showAvailableHours = (selectedDate) => {
    const availableHoursContainer = document.getElementById('available-hours-container');
    getApprovedReservations(selectedDate).then(approvedReservations => {
        const availableHoursHTML = `
            <h3>Disponibles ${selectedDate}</h3>
            <div class="hours-container">
                ${generateAvailableHours(selectedDate, approvedReservations)}
            </div>
        `;
        availableHoursContainer.innerHTML = availableHoursHTML;
        
        const hourSlots = document.querySelectorAll('.hour-slot.available');
        hourSlots.forEach(slot => {
            slot.addEventListener('click', function () {
                const allSlots = document.querySelectorAll('.hour-slot.available');
                allSlots.forEach(slot => slot.classList.remove('selected'));
                this.classList.add('selected');
                selectedTime = this.getAttribute('data-time');
                console.log('Hora seleccionada:', selectedTime);
                document.getElementById('selected-time').textContent = `Hora seleccionada: ${selectedTime}`;
                document.getElementById('reserve-btn').disabled = false;
            });
        });
    });
};

const generateAvailableHours = (selectedDate, approvedReservations) => {
    let hoursHTML = '';
    for (let i = 8; i <= 18; i++) {
        const timeSlot = `${i}:00`;
        if (approvedReservations.some(reservation => reservation.time === timeSlot)) {
            hoursHTML += `<div class="hour-slot unavailable">${timeSlot} - No disponible</div>`;
        } else {
            hoursHTML += `<div class="hour-slot available" data-time="${timeSlot}">${timeSlot} - Disponible</div>`;
        }
    }
    return hoursHTML;
};

const reserve = () => {
    if (!selectedTime) {
        alert('Por favor, selecciona una hora antes de reservar.');
        return;
    }
    fetch('/reserve', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            date: selectedDate,
            time: selectedTime
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('Reserva solicitada con éxito.');
            updateCalendar();
            showApprovedReservations(selectedDate);
            document.getElementById('selected-time').textContent = '';
            document.getElementById('reserve-btn').disabled = true;
            selectedTime = null;
            document.querySelectorAll('.hour-slot').forEach(slot => {
                slot.classList.remove('selected');
            });
        } else {
            alert('Error al realizar la reserva. Intenta nuevamente.');
        }
    })
    .catch(error => {
        console.error('Error al realizar la reserva:', error);
        alert('Hubo un error al realizar la reserva. Intenta nuevamente.');
    });
};

const showApprovedReservations = (selectedDate) => {
    const approvedReservationsContainer = document.getElementById('approved-reservations');
    getApprovedReservations(selectedDate).then(approvedReservations => {
        const approvedReservationsHTML = approvedReservations.map(reservation => {
            return `<p>${reservation.time} - Reservado por: ${reservation.user.username}</p>`;
        }).join('');
        approvedReservationsContainer.innerHTML = approvedReservationsHTML || '<p>No hay reservas aprobadas para este día.</p>';
    }).catch(err => {
        console.error('Error al obtener reservas aprobadas:', err);
        approvedReservationsContainer.innerHTML = '<p>Error al cargar las reservas.</p>';
    });
};

const changeMonth = (direction) => {
    if (direction === 'prev') {
        month -= 1;
        if (month < 0) {
            month = 11;
            year -= 1;
        }
    } else if (direction === 'next') {
        month += 1;
        if (month > 11) {
            month = 0;
            year += 1;
        }
    }
    updateCalendar();
};

const currentDate = new Date();
function renderCalendar() {
    const days = document.querySelectorAll('.calendar-day'); 

    days.forEach(day => {
        const dayDate = new Date(day.getAttribute('data-date')); 
        if (isPastDate(dayDate)) {
            day.classList.add('disabled');
            day.style.backgroundColor = '#ccc'; 
            day.style.pointerEvents = 'none';
        }
    });
}
renderCalendar();


document.addEventListener('DOMContentLoaded', function () {
    console.log('Calendario cargado');
    updateCalendar();

    document.getElementById('prev-month').addEventListener('click', () => changeMonth('prev'));
    document.getElementById('next-month').addEventListener('click', () => changeMonth('next'));
});

document.getElementById('reserve-btn').addEventListener('click', reserve);
