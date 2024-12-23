from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from .models import News
from .serializers import NewsSerializer
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Max, Count, Avg
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger



@csrf_exempt
def NewsApi(request, id=0):
    try:
        if request.method == "GET":
            if id == 0:  # Retrieve all news
                news = News.objects.all()
                news_serializer = NewsSerializer(news, many=True)
                return JsonResponse(news_serializer.data, safe=False)
            else:  # Retrieve a single news item by ID
                try:
                    news = News.objects.get(id=id)  # Ensure correct field name for lookup
                    news_serializer = NewsSerializer(news)
                    return JsonResponse(news_serializer.data, safe=False)
                except News.DoesNotExist:
                    return JsonResponse({"error": "News item not found"}, status=404)

        elif request.method == "POST":
            # Handle POST request to create a new news item
            news_data = JSONParser().parse(request)
            news_serializer = NewsSerializer(data=news_data)
            if news_serializer.is_valid():
                news_serializer.save()
                return JsonResponse("Added Successfully", safe=False)
            return JsonResponse("Fail To Add", safe=False)

        elif request.method == "PUT":
            # Handle PUT request to update a news item
            news_data = JSONParser().parse(request)
            news = News.objects.get(id=news_data["id"])
            news_serializer = NewsSerializer(news, data=news_data)
            if news_serializer.is_valid():
                news_serializer.save()
                return JsonResponse("Update Successfully", safe=False)
            return JsonResponse("Failed to Update", safe=False)

        elif request.method == "DELETE":
            # Handle DELETE request to delete a news item
            news = News.objects.get(id=id)
            news.delete()
            return JsonResponse("Deleted Successfully", safe=False)

    except News.DoesNotExist:
        # Handle case where news item is not found
        return JsonResponse("News item not found", status=404)
    except Exception as e:
        # Catch any other exceptions
        return JsonResponse(f"Error occurred: {str(e)}", status=500)

    
@csrf_exempt
def ReactionApi(request, id=0):
    try:
        if request.method == "PUT":
            news_data = JSONParser().parse(request)
            news_id = news_data.get("id", id)
            news = News.objects.get(id=news_id)  # Assumes 'id' for lookup
            
            action = news_data.get("action")  # Expecting 'like', 'dislike', or 'view'

            if action == "like":
                news.like += 1
                news.save()
                return JsonResponse({"message": "Like incremented", "like_count": news.like}, safe=False)
            
            elif action == "dislike":
                news.dislike += 1
                news.save()
                return JsonResponse({"message": "Dislike incremented", "dislike_count": news.dislike}, safe=False)
            
            elif action == "view":
                news.views += 1
                news.save()
                return JsonResponse({"message": "View incremented", "view_count": news.views}, safe=False)
            
            else:
                return JsonResponse({"error": "Invalid action"}, status=400)
        
        return JsonResponse({"error": "Invalid method"}, status=405)

    except News.DoesNotExist:
        return JsonResponse({"error": "News item not found"}, status=404)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
    

@csrf_exempt
def PaginatedNewsApi(request):
    try:
        # Get query parameters
        page = request.GET.get("page", 1)  # Default to page 1
        tags = request.GET.get("tags", None)  # Optional filtering by tags

        # Filter news by tags if provided
        if tags:
            news_queryset = News.objects.filter(tags__icontains=tags)  # 'icontains' for partial match
        else:
            news_queryset = News.objects.all()

        # Paginate the results
        paginator = Paginator(news_queryset, 3)  # 3 items per page
        try:
            news = paginator.page(page)
        except PageNotAnInteger:
            return JsonResponse({"error": "Invalid page number"}, status=400)
        except EmptyPage:
            return JsonResponse({"error": "Page not found"}, status=404)

        # Serialize the paginated data
        news_serializer = NewsSerializer(news, many=True)

        # Return paginated response
        return JsonResponse({
            "total_pages": paginator.num_pages,
            "current_page": int(page),
            "total_items": paginator.count,
            "news": news_serializer.data
        }, safe=False)

    except Exception as e:
        return JsonResponse({"error": f"Error occurred: {str(e)}"}, status=500)



@csrf_exempt
def StatisticsView(request):
    if request.method == "GET":  # Ensure only GET requests are handled
        try:
            # Calculate statistics
            total_news = News.objects.count()  # Total number of news items
            avg_views = News.objects.aggregate(Avg('views'))['views__avg'] or 0  # Average number of views
            avg_likes = News.objects.aggregate(Avg('like'))['like__avg'] or 0  # Average number of likes
            avg_dislikes = News.objects.aggregate(Avg('dislike'))['dislike__avg'] or 0  # Average number of dislikes
            most_viewed = News.objects.order_by('-views').first()  # Most viewed news

            # Prepare response data
            data = {
                "total_news": total_news,
                "avg_views": round(avg_views, 1),
                "avg_likes": round(avg_likes, 1),
                "avg_dislikes": round(avg_dislikes, 1),
                "most_viewed": {
                    "title": most_viewed.title if most_viewed else None,
                    "views": most_viewed.views if most_viewed else 0,
                } if most_viewed else None,
            }

            return JsonResponse(data, safe=False)

        except Exception as e:
            return JsonResponse({"error": f"Error occurred: {str(e)}"}, status=500)

    return JsonResponse({"error": "Invalid method"}, status=405)