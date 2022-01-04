require "test_helper"

class CookiesControllerTest < ActionDispatch::IntegrationTest
  test "should get new" do
    get cookies_new_url
    assert_response :success
  end
end
