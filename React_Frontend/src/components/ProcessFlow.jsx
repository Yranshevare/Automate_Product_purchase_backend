// ProcessFlow.jsx
import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './ProcessFlow.css';

export default function ProcessFlow() {
    const navigate = useNavigate();
    const [isNavOpen, setIsNavOpen] = useState(false);

    const steps = [
        {
            number: "1",
            title: "Create your requirement sheet",
            description: "Specify your requirement, specification and why you need this product",
            path: "/create-requirement"
        },
        {
            number: "2",
            title: "Send for primary approval",
            description: "mention the email of the person whose approval is needed",
            path: "/primary-approval"
        },
        {
            number: "3",
            title: "Request for quotetaion",
            description: "mention the email of different vendor whose quote you want",
            path: "/request-quotation"
        },
        {
            number: "4",
            title: "Quote selection",
            description: "select the specific quote for approval",
            path: "/quote-selection"
        },
        {
            number: "5",
            title: "Send for final approval",
            description: "mention the email of the person whose approval is needed",
            path: "/final-approval"
        },
        {
            number: "6",
            title: "Place a purchase Ordeer",
            description: "auto genrate a purchase order and send it to the selected vendor",
            path: "/purchase-order"
        }
    ];

    return (
        <div className="app-container">
            {/* Sidebar Navigation */}
            <div className={`sidebar ${isNavOpen ? 'open' : ''}`}>
                <div className="sidebar-content">
                <div className="user-profile">
                        <div className="avatar"></div>
                        <div className="user-info">
                            <h2>Username</h2>
                            <p>abd@gmil.com</p>
                        </div>
                    </div>
                    <div className="process-controls">
                        <div className="select-process">
                            <input className='process-select' type="text" placeholder="select the Process" />
                            <button className="add-button"><img src="react.svg" alt="" /></button>
                        </div>
                        <div className="title-inputs">
                            {[1, 2, 3].map((_, index) => (
                                <div key={index} className="title-input">
                                    <input type="text" placeholder="Title" />
                                    <span className="chevron-right"></span>
                                </div>
                            ))}
                        </div>
                    </div>
                    <button className="logout-button" onClick={() => navigate('/')}>
                        Log out
                    </button>
                </div>
            </div>

            <div className="main-content">
                {/* Header */}
                
                    
                    <button
                        className={`menu-toggle ${isNavOpen ? 'open' : ''}`}
                        onClick={() => setIsNavOpen(!isNavOpen)}
                    >
                        <span></span>
                        <span></span>
                        <span></span>
                    </button>
               

                {/* Main Process Flow */}
                <div className="process-flow">
                    <div className="title-section">
                        <h1>“Your Seamless Path to Completing a Perfect Quotation Purchase – Simple, Fast, and Secure!”</h1>
                        <img
                            src="https://s3-alpha-sig.figma.com/img/d4c4/6468/357487748ceaa640d23b8e2df289b53e?Expires=1741564800&Key-Pair-Id=APKAQ4GOSFWCW27IBOMQ&Signature=IbmlE2nxDW9oH-UbmK88z0i4RIpdQSjaqCQozVKcmZXcTbWggiJytw0ZK2QX5egmAu4ZETo8gr9Av8HIwR4dPqhRbKJAzq1wBp2nPj-kS5nQkMEmGuZSMi-yGJeIM8duqX9A6cMpHhwseEJ538XXgn2SalL6niIuf6TsqXbPCJ~erLVX5et~g0AngKGNGMc8LWTIut1RFW61a6PHj-JFbnbTqvlYOYK6RHZS0ctrxKfcfE11Qo7cm1NO7fIaOf2Ky~pi82CoZhyEsVB1FUYFpIk8865J1xrre00XfjGGBT0~K6WtIQpVDXxPzwRvP8aqL1-ISMp14vk50t7HW2E3Ng__"
                            alt="Process illustration"
                            className="illustration"
                        />
                    </div>

                   

                    <div className="timeline">
                        {steps.map((step, index) => (
                            <div key={index} className="timeline-item">
                                <div className="step-number">{step.number}</div>
                                <button
                                    className="step-button"
                                    onClick={() => navigate(step.path)}
                                >
                                    <div className="step-content">
                                        <div className="step-header">
                                            <span className="status">pending</span>
                                            <h3>{step.title}</h3>
                                            <span className="chevron-right"></span>
                                        </div>
                                        <p className="step-description">{step.description}</p>
                                    </div>
                                </button>
                            </div>
                        ))}
                    </div>

                    
                </div>
            </div>
        </div>
    );
}