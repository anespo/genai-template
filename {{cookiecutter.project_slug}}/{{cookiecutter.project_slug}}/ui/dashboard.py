"""Streamlit dashboard for GenAI testing and demos."""

import asyncio
import json
from datetime import datetime
from typing import List, Dict, Any

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from ..client import GenAIClient
from ..models import ChatMessage


# Page configuration
st.set_page_config(
    page_title="{{ cookiecutter.project_name }}",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "client" not in st.session_state:
    st.session_state.client = GenAIClient()
if "generation_history" not in st.session_state:
    st.session_state.generation_history = []


def main():
    """Main dashboard application."""
    st.title("🤖 {{ cookiecutter.project_name }}")
    st.markdown("Multi-provider GenAI testing and demonstration platform")
    
    # Sidebar
    with st.sidebar:
        st.header("Configuration")
        
        # Provider selection
        available_providers = st.session_state.client.get_available_providers()
        if not available_providers:
            st.error("No providers available. Please check your configuration.")
            return
        
        selected_provider = st.selectbox(
            "Select Provider",
            available_providers,
            key="provider_select"
        )
        
        # Model selection
        try:
            available_models = st.session_state.client.get_available_models(selected_provider)
            selected_model = st.selectbox(
                "Select Model",
                available_models,
                key="model_select"
            )
        except Exception as e:
            st.error(f"Error loading models: {e}")
            return
        
        # Generation parameters
        st.subheader("Generation Parameters")
        max_tokens = st.slider("Max Tokens", 1, 4000, 1000)
        temperature = st.slider("Temperature", 0.0, 2.0, 0.7, 0.1)
        top_p = st.slider("Top P", 0.0, 1.0, 0.9, 0.1)
        
        # Provider health check
        st.subheader("Provider Status")
        if st.button("Check Health"):
            with st.spinner("Checking provider health..."):
                health_status = asyncio.run(st.session_state.client.health_check())
                for provider, status in health_status.items():
                    status_icon = "✅" if status else "❌"
                    st.write(f"{status_icon} {provider}")
    
    # Main content tabs
    tab1, tab2, tab3, tab4 = st.tabs(["💬 Chat", "📝 Text Generation", "📊 Batch Processing", "📈 Analytics"])
    
    with tab1:
        chat_interface(selected_provider, selected_model, max_tokens, temperature, top_p)
    
    with tab2:
        text_generation_interface(selected_provider, selected_model, max_tokens, temperature, top_p)
    
    with tab3:
        batch_processing_interface(selected_provider, selected_model, max_tokens, temperature, top_p)
    
    with tab4:
        analytics_interface()


def chat_interface(provider: str, model: str, max_tokens: int, temperature: float, top_p: float):
    """Chat interface implementation."""
    st.header("💬 Interactive Chat")
    
    # System prompt
    system_prompt = st.text_area(
        "System Prompt (Optional)",
        placeholder="Enter a system prompt to set the context...",
        height=100
    )
    
    # Chat messages display
    chat_container = st.container()
    
    with chat_container:
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.write(message["content"])
                if "metadata" in message:
                    with st.expander("Metadata"):
                        st.json(message["metadata"])
    
    # Chat input
    if prompt := st.chat_input("Type your message..."):
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        with st.chat_message("user"):
            st.write(prompt)
        
        # Generate response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    # Prepare messages
                    messages = []
                    if system_prompt:
                        messages.append(ChatMessage(role="system", content=system_prompt))
                    
                    for msg in st.session_state.messages:
                        if msg["role"] != "system":
                            messages.append(ChatMessage(role=msg["role"], content=msg["content"]))
                    
                    # Generate response
                    response = asyncio.run(
                        st.session_state.client.chat(
                            messages=messages,
                            provider=provider,
                            model=model,
                            max_tokens=max_tokens,
                            temperature=temperature,
                            top_p=top_p
                        )
                    )
                    
                    st.write(response.text)
                    
                    # Add assistant message
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": response.text,
                        "metadata": {
                            "provider": response.provider,
                            "model": response.model,
                            "usage": response.usage
                        }
                    })
                    
                    # Add to history
                    st.session_state.generation_history.append({
                        "timestamp": datetime.now(),
                        "type": "chat",
                        "provider": response.provider,
                        "model": response.model,
                        "input_length": len(prompt),
                        "output_length": len(response.text),
                        "usage": response.usage
                    })
                    
                except Exception as e:
                    st.error(f"Error generating response: {e}")
    
    # Clear chat button
    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.rerun()


def text_generation_interface(provider: str, model: str, max_tokens: int, temperature: float, top_p: float):
    """Text generation interface implementation."""
    st.header("📝 Text Generation")
    
    # Input prompt
    prompt = st.text_area(
        "Enter your prompt:",
        placeholder="Write a creative story about...",
        height=150
    )
    
    col1, col2 = st.columns([1, 4])
    
    with col1:
        generate_button = st.button("Generate", type="primary")
    
    with col2:
        if st.button("Clear Output"):
            if "generation_output" in st.session_state:
                del st.session_state.generation_output
    
    if generate_button and prompt:
        with st.spinner("Generating text..."):
            try:
                response = asyncio.run(
                    st.session_state.client.generate(
                        prompt=prompt,
                        provider=provider,
                        model=model,
                        max_tokens=max_tokens,
                        temperature=temperature,
                        top_p=top_p
                    )
                )
                
                st.session_state.generation_output = response
                
                # Add to history
                st.session_state.generation_history.append({
                    "timestamp": datetime.now(),
                    "type": "generation",
                    "provider": response.provider,
                    "model": response.model,
                    "input_length": len(prompt),
                    "output_length": len(response.text),
                    "usage": response.usage
                })
                
            except Exception as e:
                st.error(f"Error generating text: {e}")
    
    # Display output
    if "generation_output" in st.session_state:
        response = st.session_state.generation_output
        
        st.subheader("Generated Text")
        st.write(response.text)
        
        # Metadata
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Generation Info")
            st.write(f"**Provider:** {response.provider}")
            st.write(f"**Model:** {response.model}")
        
        with col2:
            if response.usage:
                st.subheader("Usage Statistics")
                for key, value in response.usage.items():
                    if value is not None:
                        st.write(f"**{key.replace('_', ' ').title()}:** {value}")
        
        # Download button
        st.download_button(
            label="Download Text",
            data=response.text,
            file_name=f"generated_text_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
            mime="text/plain"
        )


def batch_processing_interface(provider: str, model: str, max_tokens: int, temperature: float, top_p: float):
    """Batch processing interface implementation."""
    st.header("📊 Batch Processing")
    
    # Input methods
    input_method = st.radio(
        "Input Method",
        ["Text Area", "File Upload"]
    )
    
    prompts = []
    
    if input_method == "Text Area":
        prompts_text = st.text_area(
            "Enter prompts (one per line):",
            placeholder="Prompt 1\nPrompt 2\nPrompt 3...",
            height=200
        )
        if prompts_text:
            prompts = [p.strip() for p in prompts_text.split('\n') if p.strip()]
    
    else:
        uploaded_file = st.file_uploader(
            "Upload text file with prompts",
            type=['txt']
        )
        if uploaded_file:
            content = uploaded_file.read().decode('utf-8')
            prompts = [p.strip() for p in content.split('\n') if p.strip()]
    
    if prompts:
        st.write(f"Found {len(prompts)} prompts")
        
        # Batch settings
        concurrent_requests = st.slider("Concurrent Requests", 1, 10, 5)
        
        if st.button("Process Batch", type="primary"):
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            try:
                status_text.text("Processing batch...")
                
                results = asyncio.run(
                    st.session_state.client.batch_generate(
                        prompts=prompts,
                        provider=provider,
                        model=model,
                        max_tokens=max_tokens,
                        temperature=temperature,
                        concurrent_requests=concurrent_requests
                    )
                )
                
                progress_bar.progress(1.0)
                status_text.text("Batch processing completed!")
                
                # Process results
                successful_results = []
                errors = []
                
                for i, result in enumerate(results):
                    if isinstance(result, Exception):
                        errors.append({"index": i, "prompt": prompts[i], "error": str(result)})
                    else:
                        successful_results.append({
                            "index": i,
                            "prompt": prompts[i],
                            "response": result.text,
                            "provider": result.provider,
                            "model": result.model,
                            "usage": result.usage
                        })
                
                # Display results
                st.subheader("Results Summary")
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("Total Prompts", len(prompts))
                with col2:
                    st.metric("Successful", len(successful_results))
                with col3:
                    st.metric("Failed", len(errors))
                
                # Successful results
                if successful_results:
                    st.subheader("Successful Results")
                    for result in successful_results:
                        with st.expander(f"Prompt {result['index'] + 1}: {result['prompt'][:50]}..."):
                            st.write("**Response:**")
                            st.write(result['response'])
                            if result['usage']:
                                st.write("**Usage:**")
                                st.json(result['usage'])
                
                # Errors
                if errors:
                    st.subheader("Errors")
                    for error in errors:
                        st.error(f"Prompt {error['index'] + 1}: {error['error']}")
                
                # Download results
                results_json = json.dumps({
                    "successful_results": successful_results,
                    "errors": errors,
                    "summary": {
                        "total": len(prompts),
                        "successful": len(successful_results),
                        "failed": len(errors)
                    }
                }, indent=2)
                
                st.download_button(
                    label="Download Results (JSON)",
                    data=results_json,
                    file_name=f"batch_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json"
                )
                
            except Exception as e:
                st.error(f"Batch processing failed: {e}")


def analytics_interface():
    """Analytics interface implementation."""
    st.header("📈 Usage Analytics")
    
    if not st.session_state.generation_history:
        st.info("No generation history available. Start using the other tabs to see analytics.")
        return
    
    # Convert history to DataFrame
    df = pd.DataFrame(st.session_state.generation_history)
    
    # Summary metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Generations", len(df))
    
    with col2:
        total_input_tokens = df['input_length'].sum()
        st.metric("Total Input Characters", total_input_tokens)
    
    with col3:
        total_output_tokens = df['output_length'].sum()
        st.metric("Total Output Characters", total_output_tokens)
    
    with col4:
        unique_providers = df['provider'].nunique()
        st.metric("Providers Used", unique_providers)
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        # Provider usage
        provider_counts = df['provider'].value_counts()
        fig_provider = px.pie(
            values=provider_counts.values,
            names=provider_counts.index,
            title="Usage by Provider"
        )
        st.plotly_chart(fig_provider, use_container_width=True)
    
    with col2:
        # Generation type
        type_counts = df['type'].value_counts()
        fig_type = px.bar(
            x=type_counts.index,
            y=type_counts.values,
            title="Usage by Type"
        )
        st.plotly_chart(fig_type, use_container_width=True)
    
    # Timeline
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df_timeline = df.groupby([df['timestamp'].dt.date, 'provider']).size().reset_index(name='count')
    
    fig_timeline = px.line(
        df_timeline,
        x='timestamp',
        y='count',
        color='provider',
        title="Usage Over Time"
    )
    st.plotly_chart(fig_timeline, use_container_width=True)
    
    # Detailed history
    st.subheader("Generation History")
    st.dataframe(
        df[['timestamp', 'type', 'provider', 'model', 'input_length', 'output_length']],
        use_container_width=True
    )
    
    # Clear history button
    if st.button("Clear History"):
        st.session_state.generation_history = []
        st.rerun()


if __name__ == "__main__":
    main()
