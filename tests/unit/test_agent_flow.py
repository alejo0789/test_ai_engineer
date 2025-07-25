# test_crew_minimal.py
"""
Minimal test for CrewAI - Super simple to understand and run.
Tests the basic functionality without complex mocking.
"""

def test_imports():
    """Test 1: Can we import the main components?"""
    print("🔍 Test 1: Testing imports...")
    
    try:
        from src.agents.tools.semantic_retrieval_tool import SemanticRetrievalTool
        print("✅ SemanticRetrievalTool imported successfully")
    except Exception as e:
        print(f"❌ Failed to import SemanticRetrievalTool: {e}")
        return False
    
    try:
        from src.agents.crew_test import ProductQueryCrew
        print("✅ ProductQueryCrew imported successfully") 
    except Exception as e:
        print(f"❌ Failed to import ProductQueryCrew: {e}")
        return False
    
    return True


def test_tool_basic():
    """Test 2: Can the semantic tool be created and used?"""
    print("\n🔍 Test 2: Testing SemanticRetrievalTool...")
    
    try:
        from src.agents.tools.semantic_retrieval_tool import SemanticRetrievalTool
        
        # Create the tool
        tool = SemanticRetrievalTool()
        print("✅ Tool created successfully")
        
        # Check it has the right attributes
        if hasattr(tool, 'name') and hasattr(tool, '_run'):
            print("✅ Tool has required attributes")
        else:
            print("❌ Tool missing required attributes")
            return False
            
        # Check the name
        if "Semantic" in tool.name:
            print("✅ Tool name is correct")
        else:
            print("❌ Tool name is unexpected")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Tool test failed: {e}")
        return False


def test_tool_with_mock():
    """Test 3: Can the tool work with mocked retriever?"""
    print("\n🔍 Test 3: Testing tool with mock data...")
    
    try:
        from unittest.mock import patch
        from src.agents.tools.semantic_retrieval_tool import SemanticRetrievalTool
        
        # Mock the retriever to return test data
        with patch('src.agents.tools.semantic_retrieval_tool.product_retriever') as mock_retriever:
            # Set up fake return data
            mock_retriever.get_relevant_context.return_value = [
                {
                    "id": "1",
                    "title": "Test Shampoo",
                    "description": "A great test shampoo",
                    "_score": 0.1
                }
            ]
            
            # Test the tool
            tool = SemanticRetrievalTool()
            result = tool._run("test query")
            
            # Check the result
            if isinstance(result, list) and len(result) == 1:
                print("✅ Tool returned correct result format")
                
                if result[0]["title"] == "Test Shampoo":
                    print("✅ Tool returned correct data")
                    return True
                else:
                    print("❌ Tool returned wrong data")
                    return False
            else:
                print("❌ Tool returned wrong format")
                return False
                
    except Exception as e:
        print(f"❌ Mock test failed: {e}")
        return False


def test_crew_creation():
    """Test 4: Can we create a ProductQueryCrew?"""
    print("\n🔍 Test 4: Testing ProductQueryCrew creation...")
    
    try:
        from unittest.mock import patch, MagicMock
        from src.agents.crew_test import ProductQueryCrew
        
        # Mock all the dependencies
        with patch('src.agents.crew_test.indexer') as mock_indexer:
            mock_indexer.index_products.return_value = None
            
            with patch('src.agents.crew_test.settings') as mock_settings:
                mock_settings.GOOGLE_API_KEY = "fake_key"
                mock_settings.GEMINI_MODEL_NAME = "fake_model"
                
                with patch('src.agents.crew_test.yaml.safe_load') as mock_yaml:
                    # Fake YAML configs
                    mock_yaml.side_effect = [
                        {'retriever_agent': {'role': 'test'}, 'responder_agent': {'role': 'test'}},
                        {'retrieve_product_context': {'description': 'test'}, 'generate_product_response': {'description': 'test'}}
                    ]
                    
                    with patch('src.agents.crew_test.Agent') as mock_agent:
                        mock_agent.return_value = MagicMock()
                        
                        with patch('src.agents.crew_test.LLM') as mock_llm:
                            mock_llm.return_value = MagicMock()
                            
                            # Try to create the crew
                            crew = ProductQueryCrew()
                            
                            if crew is not None:
                                print("✅ ProductQueryCrew created successfully")
                                
                                # Check it has the required methods
                                if hasattr(crew, 'run_crew'):
                                    print("✅ Crew has run_crew method")
                                    return True
                                else:
                                    print("❌ Crew missing run_crew method")
                                    return False
                            else:
                                print("❌ Failed to create crew")
                                return False
                                
    except Exception as e:
        print(f"❌ Crew creation test failed: {e}")
        return False


def test_crew_execution():
    """Test 5: Can the crew execute a query?"""
    print("\n🔍 Test 5: Testing crew execution...")
    
    try:
        from unittest.mock import patch, MagicMock
        from src.agents.crew_test import ProductQueryCrew
        
        # Mock everything needed for crew execution
        with patch('src.agents.crew_test.indexer') as mock_indexer:
            mock_indexer.index_products.return_value = None
            
            with patch('src.agents.crew_test.settings') as mock_settings:
                mock_settings.GOOGLE_API_KEY = "fake_key"
                mock_settings.GEMINI_MODEL_NAME = "fake_model"
                
                with patch('src.agents.crew_test.yaml.safe_load') as mock_yaml:
                    mock_yaml.side_effect = [
                        {'retriever_agent': {'role': 'test'}, 'responder_agent': {'role': 'test'}},
                        {'retrieve_product_context': {'description': '{query}'}, 'generate_product_response': {'description': '{query} {context}'}}
                    ]
                    
                    with patch('src.agents.crew_test.Agent') as mock_agent:
                        mock_agent.return_value = MagicMock()
                        
                        with patch('src.agents.crew_test.LLM') as mock_llm:
                            mock_llm.return_value = MagicMock()
                            
                            with patch('src.agents.crew_test.Crew') as mock_crew_class:
                                with patch('src.agents.crew_test.Task') as mock_task:
                                    # Mock the crew execution
                                    mock_crew_instance = MagicMock()
                                    mock_crew_instance.kickoff.return_value = "I recommend Zubale Shampoo"
                                    mock_crew_class.return_value = mock_crew_instance
                                    
                                    mock_task.return_value = MagicMock()
                                    
                                    # Create and run crew
                                    crew = ProductQueryCrew()
                                    result = crew.run_crew(
                                        user_id="test_user",
                                        query="What shampoo is good?"
                                    )
                                    
                                    # Check result
                                    if isinstance(result, str) and len(result) > 0:
                                        print("✅ Crew executed successfully")
                                        print(f"   Result: {result}")
                                        return True
                                    else:
                                        print("❌ Crew returned invalid result")
                                        return False
                                        
    except Exception as e:
        print(f"❌ Crew execution test failed: {e}")
        return False


def main():
    """Run all the simple tests."""
    print("🚀 Starting Simple CrewAI Tests")
    print("=" * 50)
    
    tests = [
        test_imports,
        test_tool_basic,
        test_tool_with_mock,
        test_crew_creation,
        test_crew_execution
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            if test():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"❌ Test {test.__name__} crashed: {e}")
            failed += 1
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed} passed, {failed} failed")
    
    if failed == 0:
        print("🎉 All tests passed! Your crew is working!")
        return True
    else:
        print("😞 Some tests failed. Check the errors above.")
        return False


if __name__ == "__main__":
    success = main()
    
    if not success:
        print("\n💡 Tips to fix failures:")
        print("1. Make sure all imports work")
        print("2. Check that your .env file has GOOGLE_API_KEY")
        print("3. Ensure all YAML config files exist")
        print("4. Install missing packages: pip install crewai pytest")
    
    exit(0 if success else 1)