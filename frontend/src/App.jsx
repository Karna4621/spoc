import React, { useState } from 'react';
import BookingForm from './components/BookingForm';
import SpocCard from './components/SpocCard';
import BookingModal from './components/BookingModal';
import { clientApi, spocApi, bookingApi } from './services/api';
import './App.css';

function App() {
  const [step, setStep] = useState('form');
  const [clientData, setClientData] = useState(null);
  const [clientId, setClientId] = useState(null);
  const [spocs, setSpocs] = useState([]);
  const [selectedSpoc, setSelectedSpoc] = useState(null);
  const [selectedSlot, setSelectedSlot] = useState(null);
  const [showModal, setShowModal] = useState(false);
  const [bookingResult, setBookingResult] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleClientSubmit = async (formData) => {
    setIsLoading(true);
    setError(null);
    try {
      const clientResponse = await clientApi.create(formData);
      setClientId(clientResponse.data.client_id);
      setClientData(formData);

      // Fetch SPOCs by solution type
      const spocsResponse = await spocApi.getAll({ solution_type: formData.solution_type });

      // Fetch availability for each SPOC
      const spocsWithAvailability = await Promise.all(
        spocsResponse.data.map(async (spoc) => {
          try {
            const availabilityResponse = await spocApi.getAvailability(
              spoc.spoc_id,
              new Date().toISOString(),
              new Date(Date.now() + 14 * 24 * 60 * 60 * 1000).toISOString()
            );
            return availabilityResponse.data;
          } catch {
            return { ...spoc, available_slots: [] };
          }
        })
      );

      setSpocs(spocsWithAvailability);
      setStep('spocs');
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to process request.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleSlotSelection = (spocId, slot) => {
    const spoc = spocs.find(s => s.spoc_id === spocId);
    setSelectedSpoc(spoc);
    setSelectedSlot(slot);
    setShowModal(true);
  };

  const handleBookingConfirm = async (meetingType) => {
    setIsLoading(true);
    setError(null);
    try {
      const bookingData = {
        client_id: clientId,
        spoc_id: selectedSpoc.spoc_id,
        slot_id: selectedSlot.slot_id,
        meeting_type: meetingType
      };
      const response = await bookingApi.create(bookingData);
      setBookingResult(response.data);
      setShowModal(false);
      setStep('success');
    } catch (err) {
      setError(err.response?.data?.detail || 'Booking failed.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleReset = () => {
    setStep('form');
    setClientData(null);
    setClientId(null);
    setSpocs([]);
    setSelectedSpoc(null);
    setSelectedSlot(null);
    setBookingResult(null);
    setError(null);
  };

  return (
    <div className="app">
      <header className="app-header">
        <h1>SPOC Booking Platform</h1>
        <p>Schedule demos and POCs with our product experts</p>
      </header>

      <main className="app-main">
        {error && (
          <div className="error-banner">
            <span>⚠️ {error}</span>
            <button onClick={() => setError(null)}>×</button>
          </div>
        )}

        {step === 'form' && <BookingForm onSubmit={handleClientSubmit} isLoading={isLoading} />}

        {step === 'spocs' && (
          <div className="spocs-section">
            <div className="section-header">
              <h2>Available SPOCs</h2>
              <button className="btn-secondary" onClick={handleReset}>← Back to Form</button>
            </div>

            {spocs.length > 0 ? (
              <div className="spocs-grid">
                {spocs.map(spoc => (
                  <SpocCard key={spoc.spoc_id} spoc={spoc} onSelectSlot={handleSlotSelection} />
                ))}
              </div>
            ) : (
              <div className="no-results">
                <p>No SPOCs available for the selected criteria.</p>
                <button className="btn-primary" onClick={handleReset}>Try Different Options</button>
              </div>
            )}
          </div>
        )}

        {step === 'success' && bookingResult && (
          <div className="success-section">
            <div className="success-icon">✓</div>
            <h2>Booking Confirmed!</h2>
            <p>Your demo has been successfully scheduled.</p>

            <div className="success-details">
              <div className="detail-box">
                <h3>Booking ID</h3>
                <p className="highlight">{bookingResult.booking_id}</p>
              </div>

              <div className="detail-box">
                <h3>SPOC</h3>
                <p>{bookingResult.spoc_name}</p>
              </div>

              <div className="detail-box">
                <h3>Date & Time</h3>
                <p>{new Date(bookingResult.start_time).toLocaleString()}</p>
              </div>

              {bookingResult.meeting_link && (
                <div className="detail-box meeting-link-box">
                  <h3>Meeting Link</h3>
                  <a href={bookingResult.meeting_link} target="_blank" rel="noopener noreferrer" className="meeting-link">
                    {bookingResult.meeting_link}
                  </a>
                  <p className="info-text">A calendar invite with this link has been sent to your email.</p>
                </div>
              )}
            </div>

            <button className="btn-primary" onClick={handleReset}>Schedule Another Demo</button>
          </div>
        )}
      </main>

      {showModal && selectedSpoc && selectedSlot && (
        <BookingModal
          isOpen={showModal}
          onClose={() => setShowModal(false)}
          spocName={selectedSpoc.name}
          slotTime={selectedSlot.start_time}
          onConfirm={handleBookingConfirm}
          isLoading={isLoading}
        />
      )}
    </div>
  );
}

export default App;
