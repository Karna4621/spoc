import React, { useState } from 'react';
import './BookingForm.css';

const BookingForm = ({ onSubmit, isLoading }) => {
  const [formData, setFormData] = useState({
    company_name: '',
    contact_name: '',
    contact_email: '',
    contact_phone: '',
    industry: '',
    budget_range: '',
    decision_timeline: '',
    solution_type: ''
  });
  
  const [errors, setErrors] = useState({});

  const solutionTypes = [
    'Cloud Infrastructure',
    'Security Solutions',
    'Data Analytics',
    'Automation',
    'Custom Solutions'
  ];

  const budgetRanges = [
    'Under $50K',
    '$50K - $250K',
    '$250K - $1M',
    '$1M+'
  ];

  const timelines = [
    'This Week',
    'Next Week',
    'This Month',
    'Open Timeline'
  ];

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
    if (errors[name]) {
      setErrors(prev => ({ ...prev, [name]: null }));
    }
  };

  const validate = () => {
    let newErrors = {};
    
    if (!formData.company_name.trim()) newErrors.company_name = 'Company name is required';
    if (!formData.contact_email.trim()) {
      newErrors.contact_email = 'Email is required';
    } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(formData.contact_email)) {
      newErrors.contact_email = 'Invalid email format';
    }
    if (!formData.solution_type) newErrors.solution_type = 'Please select a solution type';
    if (!formData.budget_range) newErrors.budget_range = 'Please select a budget range';
    if (!formData.decision_timeline) newErrors.decision_timeline = 'Please select a timeline';

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (validate()) {
      onSubmit(formData);
    }
  };

  return (
    <form className="booking-form" onSubmit={handleSubmit}>
      <h2>Client Information</h2>
      <p className="form-subtitle">Fill in the details to find available SPOCs</p>

      <div className="form-grid">
        <div className="form-group">
          <label htmlFor="company_name">Company Name <span className="required">*</span></label>
          <input type="text" id="company_name" name="company_name" value={formData.company_name} onChange={handleChange} className={errors.company_name ? 'error' : ''} />
          {errors.company_name && <span className="error-message">{errors.company_name}</span>}
        </div>

        <div className="form-group">
          <label htmlFor="contact_name">Contact Name</label>
          <input type="text" id="contact_name" name="contact_name" value={formData.contact_name} onChange={handleChange} />
        </div>

        <div className="form-group">
          <label htmlFor="contact_email">Contact Email <span className="required">*</span></label>
          <input type="email" id="contact_email" name="contact_email" value={formData.contact_email} onChange={handleChange} className={errors.contact_email ? 'error' : ''} />
          {errors.contact_email && <span className="error-message">{errors.contact_email}</span>}
        </div>

        <div className="form-group">
          <label htmlFor="contact_phone">Contact Phone</label>
          <input type="tel" id="contact_phone" name="contact_phone" value={formData.contact_phone} onChange={handleChange} />
        </div>

        <div className="form-group">
          <label htmlFor="solution_type">Solution Type <span className="required">*</span></label>
          <select id="solution_type" name="solution_type" value={formData.solution_type} onChange={handleChange} className={errors.solution_type ? 'error' : ''}>
            <option value="">Select solution type</option>
            {solutionTypes.map(type => <option key={type} value={type}>{type}</option>)}
          </select>
          {errors.solution_type && <span className="error-message">{errors.solution_type}</span>}
        </div>

        <div className="form-group">
          <label htmlFor="budget_range">Budget Range <span className="required">*</span></label>
          <select id="budget_range" name="budget_range" value={formData.budget_range} onChange={handleChange} className={errors.budget_range ? 'error' : ''}>
            <option value="">Select budget range</option>
            {budgetRanges.map(range => <option key={range} value={range}>{range}</option>)}
          </select>
          {errors.budget_range && <span className="error-message">{errors.budget_range}</span>}
        </div>

        <div className="form-group">
          <label htmlFor="decision_timeline">Decision Timeline <span className="required">*</span></label>
          <select id="decision_timeline" name="decision_timeline" value={formData.decision_timeline} onChange={handleChange} className={errors.decision_timeline ? 'error' : ''}>
            <option value="">Select timeline</option>
            {timelines.map(tl => <option key={tl} value={tl}>{tl}</option>)}
          </select>
          {errors.decision_timeline && <span className="error-message">{errors.decision_timeline}</span>}
        </div>

        <div className="form-group">
          <label htmlFor="industry">Industry</label>
          <input type="text" id="industry" name="industry" value={formData.industry} onChange={handleChange} />
        </div>
      </div>

      <button type="submit" disabled={isLoading}>{isLoading ? 'Loading...' : 'Find Available SPOCs'}</button>
    </form>
  );
};

export default BookingForm;
