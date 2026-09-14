from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from blog.models import Post, Comment
from blog.serializers import CommentsSerializer
from portfolio.models import Project, Skill
from contact.models import ContactMessage
from contact.serializers import ContactsSerializer
from django.db.models import Count, Sum, Q
from django.db.models.functions import TruncMonth
from django.utils import timezone
from datetime import timedelta



class Dashboard(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        '''
        Combine the query-aggregations accordingly.
        Posts: total_posts, published_posts, draft_posts, total_likes, total_views, top_posts, posts_per_month
        Project: total_projects
        Skill: total_skills
        Comment: total_comments, pending_comments, recent_comments
        ContactMessage: unread_messages
        '''
        post_stats = Post.objects.select_related('likesNviews').aggregate(
            total_posts=Count('id'),
            published_posts=Count('id', filter=Q(status='published')),
            draft_posts=Count('id', filter=Q(status='draft')),
            total_likes=Sum('likesNviews__likes_count'),
            total_views=Sum('likesNviews__views_count')
        )

        # Display top 5 posts based on total_views
        top_posts = Post.objects.select_related('likesNviews').order_by('-likesNviews__views_count')[:5].values('title','slug','likesNviews__views_count','likesNviews__likes_count')

        project_stats = Project.objects.aggregate(total_projects=Count('id'))

        skill_stats = Skill.objects.aggregate(total_skills=Count('id'))

        comments_stats = Comment.objects.aggregate(
            total_comments=Count('id'),
            pending_comments=Count('id', filter=Q(is_approved=False)),
        )

        # Latest 5 comments
        recent_comments = Comment.objects.order_by('-created_at')[:5]
        recent_comments_serialized = CommentsSerializer(recent_comments, many=True)

        # Unread messages
        unread_messages = ContactMessage.objects.filter(is_read=False)
        unread_messages_serialized = ContactsSerializer(unread_messages, many=True)

        # Posts per month (last 6 months)
        six_months_ago = timezone.now() - timedelta(days=6*30)
        posts_per_month = Post.objects.filter(
            created_at__gte=six_months_ago
        ).annotate(
            month=TruncMonth('created_at')
        ).values(
            'month'
        ).annotate(
            counts=Count('month')
        )

        return Response(data={
            'post_stats': post_stats,
            'top_posts': top_posts,
            'project_stats': project_stats,
            'skill_stats': skill_stats,
            'comments_stats': comments_stats,
            'recent_comments': recent_comments_serialized.data,
            'unread_messages': unread_messages_serialized.data,
            'posts_per_month': posts_per_month,
        }, status=status.HTTP_200_OK)