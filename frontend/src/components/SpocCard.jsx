import React, { useState } from 'react';
import './SpocCard.css';

const SpocCard = ({ spoc, onSelectSlot }) => {
  const [selectedSlot, setSelectedSlot] = useState(null);

  const formatDateTime = (dateString) => {
    const date = new Date(dateString);
    return {
      date: date.toLocaleDateString('en-US', { weekday: 'short', month: 'short', day: 'numeric' }),
      time: date.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' })
    };
  };

  const handleSlotClick = (slot) => {
    setSelectedSlot(slot.slot_id);
    onSelectSlot(spoc.spoc_id, slot);
  };

  return (
    <div className="spoc-card">
      <div className="spoc-header">
        <div className="spoc-avatar">
          {spoc.name.charAt(0).toUpperCase()}
        </div>
        <div className="spoc-info">
          <h3>{spoc.name}</h3>
          <p className="spoc-expertise">{spoc.expertise}</p>
          {spoc.specialization && <p className="spoc-specialization">{spoc.specialization}</p>}
        </div>
      </div>

      <div className="spoc-contact">
        <span className="contact-label">Email:</span>
        <a href={`mailto:${spoc.email}`}>{spoc.email}</a>
      </div>

      <div className="availability-section">
        <h4>Available Time Slots</h4>
        {spoc.available_slots && spoc.available_slots.length > 0 ? (
          <div className="slots-container">
            {spoc.available_slots.map(slot => {
              const { date, time } = formatDateTime(slot.start_time);
              const isSelected = selectedSlot === slot.slot_id;

              return (
                <button
                  key={slot.slot_id}
                  className={`slot-button ${isSelected ? 'selected' : ''}`}
                  onClick={() => handleSlotClick(slot)}
                >
                  <div className="slot-date">{date}</div>
                  <div className="slot-time">{time}</div>
                </button>
              );
            })}
          </div>
        ) : (
          <p className="no-slots">No available slots at this time</p>
        )}
      </div>
    </div>
  );
};

export default SpocCard;
