from asgiref.sync import sync_to_async




@sync_to_async
def serializer_save(serializer):
    serializer.is_valid(raise_exception=True)
    return serializer.save()


