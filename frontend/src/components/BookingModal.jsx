import React, { useState } from 'react';
import './BookingModal.css';

const BookingModal = ({ isOpen, onClose, spocName, slotTime, onConfirm, isLoading }) => {
  const [meetingType, setMeetingType] = useState('Technical Demo');

  const meetingTypes = [
    { value: 'Quick Intro Call', duration: '30 min' },
    { value: 'Technical Demo', duration: '60 min' },
    { value: 'Deep Dive + POC Discussion', duration: '90 min' },
  ];

  if (!isOpen) return null;

  const formatDateTime = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleString('en-US', {
      weekday: 'long',
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  const handleConfirm = () => {
    onConfirm(meetingType);
  };

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={e => e.stopPropagation()}>
        <button className="modal-close" onClick={onClose}>×</button>
        
        <h2>Confirm Booking</h2>
        
        <div className="booking-details">
          <div className="detail-row">
            <span className="detail-label">SPOC:</span>
            <span className="detail-value">{spocName}</span>
          </div>

          <div className="detail-row">
            <span className="detail-label">Date & Time:</span>
            <span className="detail-value">{formatDateTime(slotTime)}</span>
          </div>

          <div className="detail-row">
            <span className="detail-label">Meeting Type:</span>
            <select
              value={meetingType}
              onChange={(e) => setMeetingType(e.target.value)}
              className="meeting-type-select"
            >
              {meetingTypes.map(type => (
                <option key={type.value} value={type.value}>
                  {type.value} ({type.duration})
                </option>
              ))}
            </select>
          </div>
        </div>

        <div className="modal-actions">
          <button className="btn-secondary" onClick={onClose} disabled={isLoading}>
            Cancel
          </button>
          <button className="btn-primary" onClick={handleConfirm} disabled={isLoading}>
            {isLoading ? 'Booking...' : 'Confirm Booking'}
          </button>
        </div>
      </div>
    </div>
  );
};

export default BookingModal;
