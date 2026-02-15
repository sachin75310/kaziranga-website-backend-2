from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .serializers import CommunityListSerializer, CommunityDetailSerializer
from .permissions import IsAdminOrStaff
from clubs.models import Community
from .pagination import CommunityPaginator


@api_view(["GET"])
def list_communities(request):
    """
    GET /api/communities/
    Returns list of all communities with optional filtering by status
    
    Query Parameters:
    - status: Filter by 'active' or 'archived' (case-insensitive)
    
    Returns: name, logo, member_count, theme, and status for each community
    """
    try:
        communities = Community.objects.all()
        
        # Filter by status if provided
        status_filter = request.GET.get('status', '').upper()
        if status_filter:
            if status_filter not in ['ACTIVE', 'ARCHIVED']:
                return Response(
                    {"error": "Invalid status. Use 'active' or 'archived'."}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            communities = communities.filter(status=status_filter)
        
        # Pagination
        paginator = CommunityPaginator()
        paginated_communities = paginator.paginate_queryset(communities, request)
        serializer = CommunityListSerializer(paginated_communities, many=True)
        
        return paginator.get_paginated_response(serializer.data)
    
    except Exception as e:
        return Response(
            {"error": "An error occurred while fetching communities."}, 
            status=status.HTTP_503_SERVICE_UNAVAILABLE
        )


@api_view(["GET"])
def retrieve_community(request, community_id):
    """
    GET /api/communities/{id}/
    Returns detailed information about a specific community
    
    Includes all community fields plus related events
    """
    try:
        community = Community.objects.get(id=community_id)
        serializer = CommunityDetailSerializer(community)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    except Community.DoesNotExist:
        return Response(
            {"error": "Community not found."}, 
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        return Response(
            {"error": "An error occurred while fetching the community."}, 
            status=status.HTTP_503_SERVICE_UNAVAILABLE
        )


@api_view(["POST"])
@permission_classes([IsAuthenticated, IsAdminOrStaff])
def create_community(request):
    """
    POST /api/communities/create/
    Creates a new community (admin/staff only)
    
    Required fields:
    - name
    - head
    - description
    - join_form_link
    - logo
    
    Optional fields:
    - member_count (default: 0)
    - status (default: ACTIVE)
    - theme (default: OTHER)
    """
    try:
        required_fields = ["name", "head", "description", "join_form_link", "logo"]
        missing_fields = [field for field in required_fields if field not in request.data]
        
        if missing_fields:
            return Response(
                {"error": f"Missing required fields: {', '.join(missing_fields)}"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer = CommunityDetailSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    except Exception as e:
        return Response(
            {"error": "An error occurred while creating the community."}, 
            status=status.HTTP_503_SERVICE_UNAVAILABLE
        )


@api_view(["PUT", "PATCH"])
@permission_classes([IsAuthenticated, IsAdminOrStaff])
def update_community(request, community_id):
    """
    PUT/PATCH /api/communities/{id}/update/
    Updates an existing community (admin/staff only)
    """
    try:
        community = Community.objects.get(id=community_id)
        
        partial = request.method == "PATCH"
        serializer = CommunityDetailSerializer(community, data=request.data, partial=partial)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    except Community.DoesNotExist:
        return Response(
            {"error": "Community not found."}, 
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        return Response(
            {"error": "An error occurred while updating the community."}, 
            status=status.HTTP_503_SERVICE_UNAVAILABLE
        )


@api_view(["DELETE"])
@permission_classes([IsAuthenticated, IsAdminOrStaff])
def delete_community(request, community_id):
    """
    DELETE /api/communities/{id}/delete/
    Deletes a community (admin/staff only)
    """
    try:
        community = Community.objects.get(id=community_id)
        community.delete()
        
        return Response(
            {"message": "Community deleted successfully."}, 
            status=status.HTTP_204_NO_CONTENT
        )
    
    except Community.DoesNotExist:
        return Response(
            {"error": "Community not found."}, 
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        return Response(
            {"error": "An error occurred while deleting the community."}, 
            status=status.HTTP_503_SERVICE_UNAVAILABLE
        )
